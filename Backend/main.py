import datetime

# We are a company that works from 9am to 1am each day in total 16 hours. 
# In 6 different stations named: S-1, S-2, Y-1, Y-2, Y-3, and Y-4. 
# 12 workers are working each day. But sometimes 13 workers so our shift times and worker number must be flexible and be changeable by admin before each working day. 
# Each day admin sends the link to the WhatsApp group and each worker opens the page and first types their name, second chooses the preferred slot for S-1, and backup choice S-1 and then respectively for other stations. 
# when every worker changes their preferred slot no more answers are accepted. 
# Then if there are workers that choose the same slot there will be a ballot between them. 
# The loser was assigned to a second choice, if there others selected that spot they were assigned to a random spot. 
# But due to workflow after a worker completes S-1 or S-2 the next shift have to be S-2 or S-1 or free shift. 

# Utility Data Structure    
class Employee:
    id: int
    name: str
    score: int

class Manager:
    employee: Employee

# Station Data Structure
class StationSlot:
    slot_index: int
    assignee_id: str

class Station:
    name: str
    slots: list[StationSlot]

class Hospital:
    name: str
    date: datetime.date
    start_time: int
    end_time: int
    headcount: int
    stations: list[Station]
    employees: list[Employee]

# Preference Data Structure
class PreferenceSlot:
    station_name: str
    first_choice_slot_index: int
    second_choice_slot_index: int

class Preference:
    owner_id: str
    slots: list[PreferenceSlot]

def allocateSlots(preferences: list[Preference]) -> Hospital:
    hospital = Hospital()
    hospital.name = "Arnavutkoy Devlet Hastanesi"
    hospital.date = datetime.date(2023, 12, 30)
    hospital.start_time = datetime.time(9, 0)
    hospital.end_time = datetime.time(21, 0)
    hospital.headcount = 5

    total_minutes = ((hospital.end_time.hour * 60) + hospital.end_time.minute) - ((hospital.start_time.hour * 60) + hospital.start_time.minute)
    slot_minute = total_minutes // hospital.headcount
    
    hospital.stations = []
    station_requests = {}
    for station_name in ["S-1", "S-2", "Y-1"]:
        curr_station = Station()
        curr_station.name = station_name
        hospital.stations.append(curr_station)

        station_requests[station_name] = []

    hospital.employees = []
    for preference in preferences:
        curr_employee = Employee()
        curr_employee.id = preference.owner_id
        hospital.employees.append(curr_employee)

        for slot in preference.slots:
            if station_requests.get(slot.station_name) != None:
                station_requests[slot.station_name].append((preference.owner_id, slot.first_choice_slot_index, slot.second_choice_slot_index))
    
    for station_name, requested_slots in station_requests.items():
        slots = [[]] * hospital.headcount
        for requested_slot in requested_slots:
            (owner_id, first_choice, second_choice) = requested_slot
            slots[first_choice].append(owner_id)