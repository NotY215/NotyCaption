// ========================================
// Audio Renamer - Handles consistent naming for audio files
// ========================================

const AudioRenamer = {
    // Rename audio file with prefix
    renameAudioFile(file, prefix = 'NotyAudio_') {
        const originalName = file.name;
        const newName = prefix + originalName;
        
        // Create new File object with new name
        const renamedFile = new File([file], newName, {
            type: file.type,
            lastModified: file.lastModified
        });
        
        console.log(`📝 Renamed: "${originalName}" → "${newName}"`);
        return renamedFile;
    },
    
    // Get original name from prefixed name
    getOriginalName(prefixedName) {
        const prefix = 'NotyAudio_';
        if (prefixedName.startsWith(prefix)) {
            return prefixedName.substring(prefix.length);
        }
        return prefixedName;
    },
    
    // Check if file already has prefix
    hasPrefix(filename, prefix = 'NotyAudio_') {
        return filename.startsWith(prefix);
    },
    
    // Generate unique filename with timestamp
    generateUniqueFilename(originalName, prefix = 'NotyAudio_') {
        const timestamp = Date.now();
        const extension = originalName.substring(originalName.lastIndexOf('.'));
        const baseName = originalName.substring(0, originalName.lastIndexOf('.'));
        return `${prefix}${baseName}_${timestamp}${extension}`;
    }
};

window.AudioRenamer = AudioRenamer;
console.log('✅ rename.js loaded');