from .main import my_meta_data, engine, EventTypeModel


my_meta_data.create_all(bind=engine)

for event_type in ['connected', 'disconnected']:
    if not EventTypeModel.find_by_name(event_type):
        new_event_type = EventTypeModel(event_type)
        new_event_type.save_to_db()
