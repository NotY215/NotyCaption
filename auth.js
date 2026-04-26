// ========================================
// NotyCaption Pro - Google Authentication Handler
// ========================================

let accessToken = null;
let tokenExpiry = null;
let userInfo = null;

// Cookie management functions
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

// Save token to localStorage and cookie
function saveToken(token, expirySeconds = 3600) {
    accessToken = token;
    tokenExpiry = Date.now() + (expirySeconds * 1000);
    
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
    localStorage.setItem(STORAGE_KEYS.TOKEN_EXPIRY, tokenExpiry.toString());
    setCookie(STORAGE_KEYS.ACCESS_TOKEN, token, 7);
    setCookie(STORAGE_KEYS.TOKEN_EXPIRY, tokenExpiry.toString(), 7);
    
    console.log('✅ Token saved');
    return true;
}

// Load saved token
function loadSavedToken() {
    let savedToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    let savedExpiry = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRY);
    
    if (!savedToken) {
        savedToken = getCookie(STORAGE_KEYS.ACCESS_TOKEN);
        savedExpiry = getCookie(STORAGE_KEYS.TOKEN_EXPIRY);
        if (savedToken) console.log('📌 Loaded token from cookie');
    }
    
    if (savedToken && savedExpiry && Date.now() < parseInt(savedExpiry)) {
        accessToken = savedToken;
        tokenExpiry = parseInt(savedExpiry);
        
        const savedUserInfo = localStorage.getItem(STORAGE_KEYS.USER_INFO);
        if (savedUserInfo) {
            try {
                userInfo = JSON.parse(savedUserInfo);
                console.log('📌 Loaded user info:', userInfo.name);
            } catch(e) {}
        }
        
        console.log('✅ Loaded valid token');
        return true;
    }
    
    console.log('⚠️ No valid saved token found');
    return false;
}

// Clear all tokens
function clearToken() {
    accessToken = null;
    tokenExpiry = null;
    userInfo = null;
    
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.TOKEN_EXPIRY);
    localStorage.removeItem(STORAGE_KEYS.USER_INFO);
    
    deleteCookie(STORAGE_KEYS.ACCESS_TOKEN);
    deleteCookie(STORAGE_KEYS.TOKEN_EXPIRY);
    deleteCookie(STORAGE_KEYS.USER_INFO);
    
    console.log('🗑️ Cleared all auth data');
}

// Get current access token
function getAccessToken() {
    if (!accessToken) loadSavedToken();
    return accessToken;
}

// Login with Google
function loginWithGoogle() {
    console.log('🔐 Starting Google login...');
    console.log('Client ID:', CONFIG.CLIENT_ID.substring(0, 20) + '...');
    console.log('Redirect URI:', CONFIG.REDIRECT_URI);
    
    const authUrl = new URL(CONFIG.AUTH_URI);
    authUrl.searchParams.append('client_id', CONFIG.CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', CONFIG.REDIRECT_URI);
    authUrl.searchParams.append('response_type', 'token');
    authUrl.searchParams.append('scope', CONFIG.SCOPES);
    authUrl.searchParams.append('include_granted_scopes', 'true');
    authUrl.searchParams.append('prompt', 'select_account');
    authUrl.searchParams.append('state', 'notycaption_login');
    
    console.log('Redirecting to Google OAuth');
    window.location.href = authUrl.toString();
}

// Get user info from Google
async function getUserInfo() {
    const token = getAccessToken();
    if (!token) return null;
    
    try {
        console.log('👤 Fetching user info...');
        const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            userInfo = await response.json();
            localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo));
            setCookie(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo), 7);
            console.log('✅ User info loaded:', userInfo.name, userInfo.email);
            return userInfo;
        } else {
            console.log('⚠️ Token invalid, status:', response.status);
            if (response.status === 401) clearToken();
            return null;
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
        return null;
    }
}

// Check if user is logged in
async function checkLoginStatus() {
    const token = getAccessToken();
    if (!token) return false;
    
    if (!userInfo) {
        return await getUserInfo() !== null;
    }
    
    return true;
}

// Logout
function logout() {
    clearToken();
    if (typeof updateUIBasedOnAuth === 'function') {
        updateUIBasedOnAuth();
    }
    if (typeof showToast === 'function') {
        showToast('✅ Logged out successfully');
    }
    window.location.hash = 'home';
}

// Export functions
window.loginWithGoogle = loginWithGoogle;
window.logout = logout;
window.checkLoginStatus = checkLoginStatus;
window.getAccessToken = getAccessToken;
window.loadSavedToken = loadSavedToken;
window.clearToken = clearToken;
window.getUserInfo = getUserInfo;