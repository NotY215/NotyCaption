// ========================================
// Colab Processing Handler
// ========================================

let colabWindow = null;
let pollInterval = null;
let activeOperationId = null;

async function openNotebookInColab(notebookDriveId) {
    const colabUrl = `https://colab.research.google.com/drive/${notebookDriveId}`;
    console.log(`📓 Opening Colab notebook: ${colabUrl}`);
    colabWindow = window.open(colabUrl, '_blank');
    return colabWindow;
}

function startPolling(operationId, operationType, onSuccess, onError) {
    let attempts = 0;
    const maxAttempts = 120; // 10 minutes max (5 seconds * 120)
    
    if (pollInterval) clearInterval(pollInterval);
    
    console.log(`📡 Starting polling for operation: ${operationId}`);
    
    pollInterval = setInterval(async () => {
        attempts++;
        
        // Check sessionStorage for result
        const resultKey = `colab_result_${operationId}`;
        const result = sessionStorage.getItem(resultKey);
        
        if (result) {
            console.log(`📥 Result received for operation ${operationId}`, result);
            clearInterval(pollInterval);
            sessionStorage.removeItem(resultKey);
            
            try {
                const data = JSON.parse(result);
                if (data.success) {
                    if (onSuccess) await onSuccess(data.file_id, data.file_name);
                    
                    // Clean up notebook file from Drive
                    const opData = JSON.parse(sessionStorage.getItem(`colab_op_${operationId}`) || '{}');
                    if (opData.notebookDriveId && typeof deleteDriveFile === 'function') {
                        await deleteDriveFile(opData.notebookDriveId);
                        console.log(`🗑️ Deleted notebook: ${opData.notebookDriveId}`);
                    }
                    sessionStorage.removeItem(`colab_op_${operationId}`);
                    
                    // Close Colab tab if still open
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
            activeOperationId = null;
            return;
        }
        
        if (attempts >= maxAttempts) {
            console.error(`⏰ Timeout for operation ${operationId}`);
            clearInterval(pollInterval);
            if (onError) onError('Timeout! Please check Colab for results.');
            activeOperationId = null;
        } else if (attempts % 12 === 0) { // Log every minute
            console.log(`⏳ Waiting for results... (${attempts * 5} seconds)`);
        }
    }, 5000);
}

async function createAndOpenColabNotebook(operationType, params, onSuccess, onError) {
    const operationId = Date.now().toString() + '_' + Math.random().toString(36).substr(2, 8);
    console.log(`🚀 Creating ${operationType} notebook with ID: ${operationId}`);
    
    try {
        // Get notebook content from ipynb.js
        const notebookJSONString = getNotebookContent(operationType, {
            audioId: params.audioId,
            language: params.language || 'en',
            wordsPerLine: params.wordsPerLine || '5',
            outputFormat: params.outputFormat || 'srt',
            operationId: operationId
        });
        
        const notebookName = `NotyCaption_${operationType}_${operationId}.ipynb`;
        console.log(`📝 Creating notebook: ${notebookName}`);
        
        // Upload notebook to Drive
        const notebookDriveId = await uploadNotebookToDrive(notebookJSONString, notebookName);
        console.log(`✅ Notebook uploaded to Drive: ${notebookDriveId}`);
        
        // Store operation data
        sessionStorage.setItem(`colab_op_${operationId}`, JSON.stringify({
            ...params,
            operationId,
            operationType,
            notebookDriveId,
            timestamp: Date.now()
        }));
        
        // Open in Colab
        await openNotebookInColab(notebookDriveId);
        
        // Start polling for results
        startPolling(operationId, operationType, onSuccess, onError);
        
        return operationId;
    } catch (error) {
        console.error('❌ Failed to create notebook:', error);
        if (onError) onError(error.message);
        return null;
    }
}

// Function to simulate result (for testing - remove in production)
function simulateColabResult(operationId, fileId, fileName) {
    const result = {
        success: true,
        file_id: fileId,
        file_name: fileName,
        timestamp: Date.now()
    };
    sessionStorage.setItem(`colab_result_${operationId}`, JSON.stringify(result));
    console.log(`🔔 Simulated result for ${operationId}`);
}

// Export functions
window.createAndOpenColabNotebook = createAndOpenColabNotebook;
window.simulateColabResult = simulateColabResult;