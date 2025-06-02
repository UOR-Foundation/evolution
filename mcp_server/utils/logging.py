"""
Logging utilities for MCP server operations.
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json
import os


class MCPFormatter(logging.Formatter):
    """Custom formatter for MCP server logs"""
    
    def __init__(self):
        super().__init__()
        self.format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "[%(filename)s:%(lineno)d] - %(message)s"
        )
    
    def format(self, record):
        # Add MCP-specific context
        if hasattr(record, 'tool_name'):
            record.message = f"[TOOL:{record.tool_name}] {record.getMessage()}"
        elif hasattr(record, 'resource_uri'):
            record.message = f"[RESOURCE:{record.resource_uri}] {record.getMessage()}"
        elif hasattr(record, 'operation_type'):
            record.message = f"[{record.operation_type}] {record.getMessage()}"
        else:
            record.message = record.getMessage()
        
        # Format timestamp
        record.asctime = datetime.fromtimestamp(record.created).strftime(
            '%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        return self.format_string % record.__dict__


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add MCP-specific fields
        if hasattr(record, 'tool_name'):
            log_entry['tool_name'] = record.tool_name
        if hasattr(record, 'resource_uri'):
            log_entry['resource_uri'] = record.resource_uri
        if hasattr(record, 'operation_type'):
            log_entry['operation_type'] = record.operation_type
        if hasattr(record, 'execution_time_ms'):
            log_entry['execution_time_ms'] = record.execution_time_ms
        if hasattr(record, 'success'):
            log_entry['success'] = record.success
        if hasattr(record, 'error_code'):
            log_entry['error_code'] = record.error_code
        
        return json.dumps(log_entry)


def setup_mcp_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    console_output: bool = True
) -> None:
    """
    Setup logging configuration for MCP server.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        json_format: Whether to use JSON formatting
        console_output: Whether to output to console
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = MCPFormatter()
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger('mcp_server').setLevel(numeric_level)
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)


def get_mcp_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for MCP operations.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"mcp_server.{name}")


class MCPLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter for MCP-specific context"""
    
    def __init__(self, logger: logging.Logger, extra: Dict[str, Any]):
        super().__init__(logger, extra)
    
    def process(self, msg, kwargs):
        # Add extra context to log record
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra'].update(self.extra)
        return msg, kwargs


def create_tool_logger(tool_name: str) -> MCPLoggerAdapter:
    """
    Create a logger adapter for tool operations.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Logger adapter with tool context
    """
    logger = get_mcp_logger('tools')
    return MCPLoggerAdapter(logger, {'tool_name': tool_name})


def create_resource_logger(resource_uri: str) -> MCPLoggerAdapter:
    """
    Create a logger adapter for resource operations.
    
    Args:
        resource_uri: URI of the resource
        
    Returns:
        Logger adapter with resource context
    """
    logger = get_mcp_logger('resources')
    return MCPLoggerAdapter(logger, {'resource_uri': resource_uri})


def create_operation_logger(operation_type: str) -> MCPLoggerAdapter:
    """
    Create a logger adapter for general operations.
    
    Args:
        operation_type: Type of operation
        
    Returns:
        Logger adapter with operation context
    """
    logger = get_mcp_logger('operations')
    return MCPLoggerAdapter(logger, {'operation_type': operation_type})


def log_tool_execution(
    logger: logging.Logger,
    tool_name: str,
    params: Dict[str, Any],
    result: Dict[str, Any],
    execution_time_ms: float,
    success: bool = True,
    error_code: Optional[str] = None
) -> None:
    """
    Log tool execution details.
    
    Args:
        logger: Logger instance
        tool_name: Name of the executed tool
        params: Tool parameters
        result: Tool execution result
        execution_time_ms: Execution time in milliseconds
        success: Whether execution was successful
        error_code: Error code if execution failed
    """
    extra = {
        'tool_name': tool_name,
        'execution_time_ms': execution_time_ms,
        'success': success,
        'operation_type': 'TOOL_EXECUTION'
    }
    
    if error_code:
        extra['error_code'] = error_code
    
    if success:
        logger.info(
            f"Tool executed successfully: {tool_name} "
            f"(params: {len(params)} items, time: {execution_time_ms:.2f}ms)",
            extra=extra
        )
    else:
        logger.error(
            f"Tool execution failed: {tool_name} "
            f"(error: {error_code}, time: {execution_time_ms:.2f}ms)",
            extra=extra
        )


def log_resource_access(
    logger: logging.Logger,
    resource_uri: str,
    access_type: str,
    success: bool = True,
    content_length: Optional[int] = None,
    error_code: Optional[str] = None
) -> None:
    """
    Log resource access details.
    
    Args:
        logger: Logger instance
        resource_uri: URI of the accessed resource
        access_type: Type of access (read, write, list)
        success: Whether access was successful
        content_length: Length of content accessed
        error_code: Error code if access failed
    """
    extra = {
        'resource_uri': resource_uri,
        'success': success,
        'operation_type': 'RESOURCE_ACCESS'
    }
    
    if error_code:
        extra['error_code'] = error_code
    
    if success:
        msg = f"Resource accessed successfully: {resource_uri} ({access_type})"
        if content_length is not None:
            msg += f" - {content_length} bytes"
        logger.info(msg, extra=extra)
    else:
        logger.error(
            f"Resource access failed: {resource_uri} ({access_type}) "
            f"- error: {error_code}",
            extra=extra
        )


def log_system_event(
    logger: logging.Logger,
    event_type: str,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log system-level events.
    
    Args:
        logger: Logger instance
        event_type: Type of system event
        message: Event message
        details: Additional event details
    """
    extra = {
        'operation_type': 'SYSTEM_EVENT',
        'event_type': event_type
    }
    
    if details:
        extra.update(details)
    
    logger.info(f"System event: {event_type} - {message}", extra=extra)


def log_performance_metrics(
    logger: logging.Logger,
    metrics: Dict[str, float]
) -> None:
    """
    Log performance metrics.
    
    Args:
        logger: Logger instance
        metrics: Performance metrics dictionary
    """
    extra = {
        'operation_type': 'PERFORMANCE_METRICS',
        **metrics
    }
    
    logger.info(f"Performance metrics: {metrics}", extra=extra)


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    message: str,
    severity: str = "INFO",
    source_ip: Optional[str] = None,
    user_agent: Optional[str] = None
) -> None:
    """
    Log security-related events.
    
    Args:
        logger: Logger instance
        event_type: Type of security event
        message: Event message
        severity: Event severity (INFO, WARNING, ERROR, CRITICAL)
        source_ip: Source IP address
        user_agent: User agent string
    """
    extra = {
        'operation_type': 'SECURITY_EVENT',
        'event_type': event_type,
        'severity': severity
    }
    
    if source_ip:
        extra['source_ip'] = source_ip
    if user_agent:
        extra['user_agent'] = user_agent
    
    log_level = getattr(logging, severity.upper(), logging.INFO)
    logger.log(log_level, f"Security event: {event_type} - {message}", extra=extra)


class PerformanceTimer:
    """Context manager for timing operations"""
    
    def __init__(self, logger: logging.Logger, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
        
        extra = {
            'operation_type': 'PERFORMANCE_TIMING',
            'operation_name': self.operation_name,
            'duration_ms': duration_ms
        }
        
        if exc_type is None:
            self.logger.debug(
                f"Operation completed: {self.operation_name} "
                f"({duration_ms:.2f}ms)",
                extra=extra
            )
        else:
            extra['error'] = str(exc_val)
            self.logger.error(
                f"Operation failed: {self.operation_name} "
                f"({duration_ms:.2f}ms) - {exc_val}",
                extra=extra
            )
    
    def get_duration_ms(self) -> Optional[float]:
        """Get operation duration in milliseconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return None
