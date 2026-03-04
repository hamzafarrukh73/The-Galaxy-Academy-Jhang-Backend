from django.utils.csp import CSP

# HOST & CORS
INSTALLED_APPS.extend(["corsheaders"])
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["*"])

# Content Security Policy
MIDDLEWARE.extend(["django.middleware.csp.ContentSecurityPolicyMiddleware"])

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE, CSP.UNSAFE_EVAL, CSP.UNSAFE_INLINE],
    "style-src": [CSP.SELF, CSP.NONCE, CSP.UNSAFE_INLINE],
    "img-src": [CSP.SELF, "data:"],
    "connect-src": [CSP.SELF],
    "font-src": [CSP.SELF],
    "frame-ancestors": [CSP.SELF],
}

# Common Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
