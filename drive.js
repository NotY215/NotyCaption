// ========================================
// Google Drive Operations
// ========================================

let currentAudioDriveId = null;

async function ensureValidToken() {
    if (!accessToken) {
        throw new Error('No access token available. Please login first.');
    }
    return true;
}

async function apiRequest(url, options = {}) {
    await ensureValidToken();
    
    const response = await fetch(url, {
        ...options,
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    
    if (response.status === 401) {
        console.log('Token expired, clearing...');
        clearToken();
        throw new Error('Authentication failed. Please login again.');
    }
    
    return response;
}

async function getOrCreateFolder(folderName) {
    await ensureValidToken();
    
    const query = `name='${folderName}' and mimeType='application/vnd.google-apps.folder' and trashed=false`;
    const response = await apiRequest(`https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(query)}&fields=files(id,name)`);
    
    const data = await response.json();
    
    if (data.files && data.files.length > 0) {
        return data.files[0].id;
    }
    
    const metadata = {
        name: folderName,
        mimeType: 'application/vnd.google-apps.folder'
    };
    
    const createResponse = await apiRequest('https://www.googleapis.com/drive/v3/files', {
        method: 'POST',
        body: JSON.stringify(metadata)
    });
    
    const folderData = await createResponse.json();
    return folderData.id;
}

async function uploadFileToDrive(file, folderId) {
    await ensureValidToken();
    
    const metadata = {
        name: file.name,
        mimeType: file.type,
        parents: [folderId]
    };
    
    const form = new FormData();
    form.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    form.append('file', file);
    
    const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${accessToken}` },
        body: form
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    return data.id;
}

async function uploadNotebookToDrive(notebookJSONString, notebookName) {
    await ensureValidToken();
    
    const folderId = await getOrCreateFolder(CONFIG.NOTEBOOK_FOLDER_NAME);
    
    const notebookBlob = new Blob([notebookJSONString], { type: 'application/json' });
    const notebookFile = new File([notebookBlob], notebookName, { type: 'application/json' });
    
    const metadata = {
        name: notebookName,
        mimeType: 'application/x-ipynb+json',
        parents: [folderId]
    };
    
    const form = new FormData();
    form.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    form.append('file', notebookFile);
    
    const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${accessToken}` },
        body: form
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
    await ensureValidToken();
    
    const response = await apiRequest(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`);
    return await response.text();
}

async function getFileDownloadUrl(fileId) {
    await ensureValidToken();
    return `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media&access_token=${accessToken}`;
}

async function deleteDriveFile(fileId) {
    await ensureValidToken();
    
    try {
        await apiRequest(`https://www.googleapis.com/drive/v3/files/${fileId}`, { method: 'DELETE' });
        console.log(`Deleted file: ${fileId}`);
    } catch (error) {
        console.error('Delete error:', error);
    }
}

async function cleanupOldNotebooks() {
    try {
        const folderId = await getOrCreateFolder(CONFIG.NOTEBOOK_FOLDER_NAME);
        const query = `'${folderId}' in parents and name contains 'NotyCaption_' and trashed=false`;
        const response = await apiRequest(`https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(query)}&fields=files(id,name)`);
        const data = await response.json();
        
        if (data.files && data.files.length > 0) {
            for (const file of data.files) {
                await deleteDriveFile(file.id);
                console.log(`🗑️ Deleted old notebook: ${file.name}`);
            }
            return data.files.length;
        }
        return 0;
    } catch (error) {
        console.log('No old notebooks to delete:', error);
        return 0;
    }
}

async function uploadAudioToDrive(file) {
    const folderId = await getOrCreateFolder(CONFIG.TEMP_FOLDER_NAME);
    const fileId = await uploadFileToDrive(file, folderId);
    currentAudioDriveId = fileId;
    return fileId;
}

// Export functions
window.uploadAudioToDrive = uploadAudioToDrive;
window.uploadNotebookToDrive = uploadNotebookToDrive;
window.getFileContent = getFileContent;
window.getFileDownloadUrl = getFileDownloadUrl;
window.deleteDriveFile = deleteDriveFile;
window.cleanupOldNotebooks = cleanupOldNotebooks;