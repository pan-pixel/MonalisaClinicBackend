"""
Custom email backend with SSL certificate verification handling.
This backend handles SSL certificate verification issues on macOS and other systems.
"""
import ssl
import logging
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
from django.conf import settings

logger = logging.getLogger('api.email_backend')


class CustomSMTPEmailBackend(SMTPEmailBackend):
    """
    Custom SMTP email backend that handles SSL certificate verification.
    For development/local environments, it can use unverified SSL context.
    For production, it should use verified SSL context.
    """
    
    def open(self):
        """
        Override open() to handle SSL certificate verification.
        """
        if self.connection:
            # Nothing to do if already connected
            return False
        
        # Get SSL verification setting from Django settings
        ssl_verify = getattr(settings, 'EMAIL_SSL_VERIFY', False)
        
        try:
            # If SSL verification is disabled, create an unverified context
            if not ssl_verify:
                logger.warning("=" * 60)
                logger.warning("SSL CERTIFICATE VERIFICATION IS DISABLED")
                logger.warning("This should only be used in development/local environments!")
                logger.warning("=" * 60)
                # Create an unverified SSL context
                self.ssl_context = ssl.create_default_context()
                self.ssl_context.check_hostname = False
                self.ssl_context.verify_mode = ssl.CERT_NONE
                logger.info("Using unverified SSL context (certificate verification disabled)")
            else:
                # Use default SSL context with verification
                try:
                    self.ssl_context = ssl.create_default_context()
                    logger.info("Using SSL context with certificate verification enabled")
                except Exception as e:
                    logger.warning(f"Failed to create default SSL context: {e}")
                    logger.warning("Falling back to unverified SSL context...")
                    # Fallback to unverified context if default context creation fails
                    self.ssl_context = ssl.create_default_context()
                    self.ssl_context.check_hostname = False
                    self.ssl_context.verify_mode = ssl.CERT_NONE
            
            # Call parent's open method
            logger.info(f"Attempting to connect to {self.host}:{self.port}")
            return super().open()
            
        except ssl.SSLError as e:
            logger.error("=" * 60)
            logger.error("SSL ERROR DURING CONNECTION")
            logger.error("=" * 60)
            logger.error(f"SSL Error: {e}")
            logger.error(f"Error Type: {type(e).__name__}")
            
            # If we're already using unverified context, don't retry
            if not ssl_verify and hasattr(self, 'ssl_context'):
                logger.error("Already using unverified SSL context. Cannot retry.")
                raise
            
            logger.warning("Retrying with unverified SSL context...")
            # Retry with unverified context
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
            try:
                result = super().open()
                logger.info("Successfully connected with unverified SSL context")
                return result
            except Exception as retry_error:
                logger.error(f"Retry also failed: {retry_error}")
                raise
        except Exception as e:
            logger.error("=" * 60)
            logger.error("ERROR OPENING EMAIL CONNECTION")
            logger.error("=" * 60)
            logger.error(f"Error Type: {type(e).__name__}")
            logger.error(f"Error Message: {str(e)}")
            raise
