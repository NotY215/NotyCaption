// ========================================
// Google Drive Operations
// ========================================

let currentAudioDriveId = null;

async function ensureValidToken() {
    let token = localStorage.getItem('notycaption_access_token');
    if (!token) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'notycaption_access_token') {
                token = decodeURIComponent(value);
                localStorage.setItem('notycaption_access_token', token);
                break;
            }
        }
    }
    
    if (!token) {
        throw new Error('No access token available. Please login first.');
    }
    
    // Verify token is still valid
    try {
        const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) {
            console.log('Token invalid, clearing...');
            localStorage.clear();
            document.cookie.split(';').forEach(c => {
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
            });
            window.location.href = 'index.html';
            throw new Error('Session expired. Please login again.');
        }
    } catch (error) {
        console.error('Token verification error:', error);
        throw new Error('Authentication failed. Please refresh and login again.');
    }
    
    return token;
}

async function getOrCreateFolder(folderName) {
    const token = await ensureValidToken();
    
    const query = `name='${folderName}' and mimeType='application/vnd.google-apps.folder' and trashed=false`;
    const response = await fetch(`https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(query)}&fields=files(id,name)`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const data = await response.json();
    
    if (data.files && data.files.length > 0) {
        console.log(`📁 Found folder: ${folderName} (ID: ${data.files[0].id})`);
        return data.files[0].id;
    }
    
    const metadata = {
        name: folderName,
        mimeType: 'application/vnd.google-apps.folder'
    };
    
    const createResponse = await fetch('https://www.googleapis.com/drive/v3/files', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(metadata)
    });
    
    const folderData = await createResponse.json();
    console.log(`📁 Created folder: ${folderName} (ID: ${folderData.id})`);
    return folderData.id;
}

async function uploadAudioToDrive(file) {
    console.log(`📤 Uploading audio: ${file.name}`);
    
    const token = await ensureValidToken();
    const folderId = await getOrCreateFolder(CONFIG.TEMP_FOLDER_NAME);
    
    const metadata = {
        name: file.name,
        mimeType: file.type,
        parents: [folderId]
    };
    
    const formData = new FormData();
    formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    formData.append('file', file);
    
    const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });
    
    if (response.status === 401) {
        console.log('Token expired during upload, redirecting to login...');
        localStorage.clear();
        document.cookie.split(';').forEach(c => {
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        });
        window.location.href = 'index.html';
        throw new Error('Session expired. Please login again.');
    }
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    currentAudioDriveId = data.id;
    console.log(`✅ Audio uploaded: ${file.name} (ID: ${data.id})`);
    return data.id;
}

async function uploadNotebookToDrive(notebookJSONString, notebookName) {
    console.log(`📤 Uploading notebook: ${notebookName}`);
    
    const token = await ensureValidToken();
    const folderId = await getOrCreateFolder(CONFIG.NOTEBOOK_FOLDER_NAME);
    
    const metadata = {
        name: notebookName,
        mimeType: 'application/x-ipynb+json',
        parents: [folderId]
    };
    
    const formData = new FormData();
    formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    formData.append('file', new Blob([notebookJSONString], { type: 'application/json' }));
    
    const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Notebook upload failed: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    console.log(`✅ Notebook uploaded: ${notebookName} (ID: ${data.id})`);
    return data.id;
}

async function getFileContent(fileId) {
    const token = await ensureValidToken();
    
    const response = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!response.ok) {
        throw new Error(`Failed to get file content: ${response.status}`);
    }
    
    return await response.text();
}

async function getFileDownloadUrl(fileId) {
    const token = await ensureValidToken();
    return `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media&access_token=${token}`;
}

async function deleteDriveFile(fileId) {
    const token = await ensureValidToken();
    
    try {
        await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log(`🗑️ Deleted file: ${fileId}`);
    } catch (error) {
        console.error('Delete error:', error);
    }
}

async function cleanupOldNotebooks() {
    try {
        const token = await ensureValidToken();
        
        const query = `name contains 'NotyCaption_' and mimeType='application/x-ipynb+json' and trashed=false`;
        const response = await fetch(`https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(query)}&fields=files(id,name,createdTime)`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const oneHourAgo = Date.now() - (60 * 60 * 1000);
        
        if (data.files && data.files.length > 0) {
            for (const file of data.files) {
                const createdTime = new Date(file.createdTime).getTime();
                if (createdTime < oneHourAgo) {
                    await deleteDriveFile(file.id);
                    console.log(`🗑️ Deleted old notebook: ${file.name}`);
                }
            }
        }
    } catch (error) {
        console.log('Cleanup error:', error);
    }
}

// Export functions
window.uploadAudioToDrive = uploadAudioToDrive;
window.uploadNotebookToDrive = uploadNotebookToDrive;
window.getFileContent = getFileContent;
window.getFileDownloadUrl = getFileDownloadUrl;
window.deleteDriveFile = deleteDriveFile;
window.cleanupOldNotebooks = cleanupOldNotebooks;

console.log('✅ drive.js loaded');