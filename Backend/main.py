import random

from Utility.types import *

def allocateSlots(station_names: List[str], preferences: List[Preference], num_slots: int) -> List[Station]:
    allocated_stations = []

    all_station_requests = {}
    for station_name in station_names:
        all_station_requests[station_name] = {}

    for preference in preferences:
        for slot in preference.slots:
            if all_station_requests.get(slot.station_name) != None:
                all_station_requests[slot.station_name][preference.owner_id] = (slot.first_choice_slot_index, slot.second_choice_slot_index)

    for station_name, station_request in all_station_requests.items():
        slots = [[]] * num_slots
        for owner_id, requested_slots in station_request.items():
            slots[requested_slots[0]].append(owner_id)

        while any(list(map(lambda slot: len(slot) > 1, slots))):
            for index, slot in enumerate(slots):
                if len(slot) > 1:
                    chosen_employee_id = slot[random.randint(1, len(slot)) - 1]
                    should_redistribute_employee_ids = list(filter(lambda id: id != chosen_employee_id, slot))

                    slots[index] = [chosen_employee_id]
                    for redistribute_id in should_redistribute_employee_ids:
                        (first_choice_slot_index, second_choice_slot_index) = station_request[redistribute_id]
                        if index == first_choice_slot_index:
                            new_index = second_choice_slot_index
                        elif any(list(map(lambda slot: len(slot) == 0, slots))):
                            for index, slot in enumerate(slots):
                                if len(slot) == 0:
                                    new_index = index
                                    break
                        else:
                            new_index = (index + 1) % num_slots

                        slots[new_index].append(redistribute_id)
        
        allocated_station = Station()
        allocated_station.name = station_name
        allocated_station.slots = []
        for index, slot in enumerate(slots):
            stationSlot = StationSlot()
            stationSlot.slot_index = index
            stationSlot.assignee_id = slot
            allocated_station.slots.append(stationSlot)
        allocated_stations.append(allocated_station)

    return allocated_stations

def getDailySchedule(station_names: List[str], employees: List[Employee], preferences: List[Preference], date: datetime.date, start_time: datetime.time, shift_length: datetime.time) -> Schedule:
    # Create the output Schedule object with empty station slots
    current_schedule = Schedule()
    current_schedule.date = date
    current_schedule.start_time = start_time
    current_schedule.shift_length = shift_length
    current_schedule.daily_stations = allocateSlots(station_names, preferences, len(employees))
    current_schedule.daily_employees = employees

    return current_schedule

if __name__ == "__main__":
    station_names = ["S-1", "S-2", "Y-1"]

    employees = []
    for i in range(8):
        employee = Employee()
        employee.id = i
        employee.name = "Employee {0}".format(i)
        employee.score = 50
        employees.append(employee)
    
    preferences = []
    for i in range(8):
        preference = Preference()
        preference.owner_id = i
        preference.slots = []
        for station_name in station_names:
            slot = PreferenceSlot()
            slot.station_name = station_name
            slot.first_choice_slot_index = random.randint(0, 7)
            slot.second_choice_slot_index = random.randint(0, 7)
            preference.slots.append(slot)
        preferences.append(preference)

    new_schedule = getDailySchedule(station_names, employees, preferences, datetime.date(2024, 1, 4), datetime.time(hour=9), datetime.time(12))
    print("Schedule for {0}/{1}/{2}, starting at {3}:{4} for a shift length of {5}:{6}".format(new_schedule.date.day, 
                                                                                               new_schedule.date.month, 
                                                                                               new_schedule.date.year,
                                                                                               new_schedule.start_time.hour,
                                                                                               new_schedule.start_time.minute,
                                                                                               new_schedule.shift_length.hour,
                                                                                               new_schedule.shift_length.minute))
    
    print("Employees:")
    for employee in new_schedule.daily_employees:
        print("- ID: {0} | Name: {1} | Score: {2}".format(employee.id, employee.name, employee.score))
        print("-- Choices:")
        for slot in preferences[employee.id].slots:
            print("--- Slot {0}: {1} and {2}".format(slot.station_name, slot.first_choice_slot_index, slot.second_choice_slot_index))
    
    print("Stations:")
    for station in new_schedule.daily_stations:
        print("- Station {0}".format(station.name))
        for slot in station.slots:
            print("-- Slot {0}: {1}".format(slot.slot_index, slot.assignee_id))
