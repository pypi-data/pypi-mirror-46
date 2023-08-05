config_manager = None
builder_service = None
retention_service = None
metrics_registrar = None
schedule_task_manager = None

# Should not be accessed directly. Use common.logger.get_logger to get instance of this logger
_logger = None