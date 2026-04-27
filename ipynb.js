// ========================================
// NotyCaption Pro - Notebook Builder
// ========================================

let captionTemplate = null;
let enhanceTemplate = null;

async function loadTemplates() {
    try {
        const captionResponse = await fetch('caption.ipynb');
        if (captionResponse.ok) {
            captionTemplate = await captionResponse.text();
            console.log('✅ caption.ipynb template loaded');
        } else {
            console.error('Failed to load caption.ipynb');
            throw new Error('caption.ipynb not found');
        }
        
        const enhanceResponse = await fetch('enhance.ipynb');
        if (enhanceResponse.ok) {
            enhanceTemplate = await enhanceResponse.text();
            console.log('✅ enhance.ipynb template loaded');
        } else {
            console.error('Failed to load enhance.ipynb');
            throw new Error('enhance.ipynb not found');
        }
        
        return true;
    } catch (error) {
        console.error('Error loading templates:', error);
        return false;
    }
}

// Extract audio name from file ID (we need to pass the actual audio name)
function getAudioName() {
    // This will be replaced by the actual audio name from the upload
    return 'audio';
}

function getNotebookContent(operationType, params) {
    let template = operationType === 'enhance' ? enhanceTemplate : captionTemplate;
    
    if (!template) {
        console.error('Template not loaded');
        return null;
    }
    
    // Get audio name from the stored file info
    let audioName = params.audioName || 'captions';
    // Remove extension if present
    audioName = audioName.replace(/\.(mp3|wav|m4a|flac|ogg|aac)$/i, '');
    
    let content = template
        .replace(/\{\{AUDIO_ID\}\}/g, params.audioId)
        .replace(/\{\{LANGUAGE\}\}/g, params.language || 'en')
        .replace(/\{\{WORDS_PER_LINE\}\}/g, params.wordsPerLine || '5')
        .replace(/\{\{OUTPUT_FORMAT\}\}/g, params.outputFormat || 'srt')
        .replace(/\{\{OPERATION_ID\}\}/g, params.operationId)
        .replace(/\{\{AUDIO_NAME\}\}/g, audioName);
    
    // Validate JSON
    try {
        JSON.parse(content);
        console.log('✅ Notebook JSON is valid');
    } catch (e) {
        console.error('Invalid notebook JSON:', e);
        throw new Error('Failed to create notebook: Invalid JSON structure');
    }
    
    return content;
}

async function cleanupOldFiles() {
    try {
        const token = localStorage.getItem('notycaption_access_token');
        if (!token) return;
        
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
                    await fetch(`https://www.googleapis.com/drive/v3/files/${file.id}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    console.log(`🗑️ Deleted old notebook: ${file.name}`);
                }
            }
        }
    } catch (error) {
        console.log('Cleanup error:', error);
    }
}

(async function init() {
    await loadTemplates();
    await cleanupOldFiles();
    console.log('✅ ipynb.js ready with T4 GPU templates');
})();

window.getNotebookContent = getNotebookContent;
window.cleanupOldFiles = cleanupOldFiles;