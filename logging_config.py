"""
Centralized logging configuration for the scraper project.
"""

import logging
import os
from datetime import datetime

def setup_logging(name: str = None, level: str = "INFO", log_to_file: bool = True) -> logging.Logger:
    """
    Set up and configure logging for the application.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to also log to a file
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name or __name__)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Set logging level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_to_file:
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create log file with timestamp
        log_filename = f"{log_dir}/scraper_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Global logger for project-wide use
def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance with the standard configuration."""
    return setup_logging(name)
