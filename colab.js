// ========================================
// Colab Processing Handler
// ========================================

let colabWindow = null;
let pollInterval = null;

async function openNotebookInColab(notebookDriveId) {
    const colabUrl = `https://colab.research.google.com/drive/${notebookDriveId}`;
    console.log(`📓 Opening Colab notebook: ${colabUrl}`);
    colabWindow = window.open(colabUrl, '_blank');
    if (!colabWindow) {
        console.warn('Popup blocked! Please allow popups for this site');
        alert('⚠️ Popup blocked! Please allow popups for this site to open Colab.\n\nYou can also click the "Open in Colab" button manually if the tab doesn\'t open.');
    }
    return colabWindow;
}

function startPolling(operationId, operationType, onSuccess, onError) {
    let attempts = 0;
    const maxAttempts = 180;
    
    if (pollInterval) clearInterval(pollInterval);
    
    console.log(`📡 Starting polling for operation: ${operationId}`);
    
    pollInterval = setInterval(async () => {
        attempts++;
        
        const result = sessionStorage.getItem(`colab_result_${operationId}`);
        if (result) {
            console.log(`📥 Result received for operation ${operationId}`);
            clearInterval(pollInterval);
            sessionStorage.removeItem(`colab_result_${operationId}`);
            
            try {
                const data = JSON.parse(result);
                if (data.success) {
                    if (onSuccess) await onSuccess(data.file_id, data.file_name);
                    
                    const opData = sessionStorage.getItem(`colab_op_${operationId}`);
                    if (opData) {
                        const opDataObj = JSON.parse(opData);
                        if (opDataObj.notebookDriveId && typeof deleteDriveFile === 'function') {
                            await deleteDriveFile(opDataObj.notebookDriveId);
                        }
                        sessionStorage.removeItem(`colab_op_${operationId}`);
                    }
                    
                    if (colabWindow && !colabWindow.closed) {
                        colabWindow.close();
                    }
                } else {
                    if (onError) onError(data.error || 'Processing failed');
                }
            } catch(e) {
                console.error('Error parsing result:', e);
                if (onError) onError('Error processing result');
            }
            pollInterval = null;
            return;
        }
        
        if (attempts >= maxAttempts) {
            console.error(`⏰ Timeout for operation ${operationId}`);
            clearInterval(pollInterval);
            if (onError) onError('Timeout! Please check Colab for results.');
            pollInterval = null;
        } else if (attempts % 12 === 0) {
            console.log(`⏳ Waiting for results... (${attempts * 5} seconds elapsed)`);
        }
    }, 5000);
}

async function createAndOpenColabNotebook(operationType, params, onSuccess, onError) {
    console.log('createAndOpenColabNotebook called with:', operationType, params);
    
    if (typeof getNotebookContent === 'undefined') {
        console.error('getNotebookContent is undefined. ipynb.js may not be loaded.');
        if (onError) onError('ipynb.js not loaded properly. Please refresh the page.');
        return null;
    }
    
    const operationId = Date.now().toString() + '_' + Math.random().toString(36).substr(2, 8);
    console.log(`🚀 Creating ${operationType} notebook with ID: ${operationId}`);
    
    try {
        const result = getNotebookContent(operationType, {
            audioId: params.audioId,
            language: params.language || 'en',
            wordsPerLine: params.wordsPerLine || '5',
            outputFormat: params.outputFormat || 'srt',
            operationId: operationId
        });
        
        let notebookJSONString, notebookName;
        
        if (typeof result === 'object' && result.content) {
            notebookJSONString = result.content;
            notebookName = result.notebookName;
        } else {
            notebookJSONString = result;
            notebookName = `NotyCaption_${operationType}_${operationId}.ipynb`;
        }
        
        if (!notebookJSONString) {
            throw new Error('Failed to get notebook content');
        }
        
        console.log(`📝 Creating notebook: ${notebookName}`);
        
        const notebookDriveId = await uploadNotebookToDrive(notebookJSONString, notebookName);
        console.log(`✅ Notebook uploaded to Drive: ${notebookDriveId}`);
        
        sessionStorage.setItem(`colab_op_${operationId}`, JSON.stringify({
            ...params,
            operationId,
            operationType,
            notebookDriveId,
            notebookName,
            timestamp: Date.now()
        }));
        
        await openNotebookInColab(notebookDriveId);
        startPolling(operationId, operationType, onSuccess, onError);
        
        return operationId;
    } catch (error) {
        console.error('❌ Failed to create notebook:', error);
        if (onError) onError(error.message);
        return null;
    }
}

// Export functions
window.createAndOpenColabNotebook = createAndOpenColabNotebook;
window.openNotebookInColab = openNotebookInColab;
window.startPolling = startPolling;

console.log('✅ colab.js loaded');