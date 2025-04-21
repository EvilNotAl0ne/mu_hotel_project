def parse_booking_data(text):
    fields = text.split(",")
    data = {
        "first_name": fields[0].strip(),
        "last_name": fields[1].strip(),
        "email": fields[2].strip(),
        "phone": fields[3].strip(),
    }
    return data