"""Page 1 specific computation logic."""

from .calculations import ERROR, VALIDATION_RULES, _format_table_value, validate_input

# ==========================================================================================
# Page 1 validation rules
# Defined here so future updates to page1 inputs only require edits in this file.
# Registered into the central VALIDATION_RULES dict so validate_input() can find them.
# When adding a new page: create pageN_calculations.py and do the same pattern.
# ==========================================================================================
VALIDATION_RULES["page1"] = {
    "table1": {
        "total_distance":           (0,    50000, float),
        "operating_speed":          (0.1,  12,    float),
        "working_days_per_year":    (1,    366,   int),
        "working_hours_per_day":    (0.1,  24,    float),
        "required_hourly_capacity": (1,    30000, int),
        "effective_cabin_capacity": (1,    300,   int),
        "cabins_per_group":         (1,    2,     int),
        "acceleration":             (0.01, 0.8,   float),
        "deceleration":             (-0.8, -0.01, float),
        "braking_deceleration":     (-3.0, -0.01, float),
        "creep_speed":              (0.01, 1.0,   float),
        "creep_distance":           (0,    200,   float),
    },
}


def compute_p1_table(page: str, input_data: dict) -> dict:
    """
    Compute outputs for Page 1 tables.
    
    Args:
        page (str): Page name ("page1")
        input_data (dict): Dictionary with table data: {"table1": {...}}
    
    Returns:
        dict: Output structure {"table2": {"station_dwell_time": value or None, ...}}
    """
    if page != "page1":
        raise ValueError(f"compute_p1_table is only for page1, but got {page}")

    # --------------------------------------------------
    # 1. Extract inputs (safe get + default None if missing)
    # --------------------------------------------------
    t1 = input_data.get("table1", {})

    total_distance            = t1.get("total_distance")
    operating_speed           = t1.get("operating_speed")
    working_days_per_year     = t1.get("working_days_per_year")
    working_hours_per_day     = t1.get("working_hours_per_day")
    required_hourly_capacity  = t1.get("required_hourly_capacity")
    effective_cabin_capacity  = t1.get("effective_cabin_capacity")
    cabins_per_group          = t1.get("cabins_per_group")
    acceleration              = t1.get("acceleration")
    deceleration              = t1.get("deceleration")
    braking_deceleration      = t1.get("braking_deceleration")
    creep_speed               = t1.get("creep_speed")
    creep_distance            = t1.get("creep_distance")

    # --------------------------------------------------
    # 2. Validate each input independently → set to ERROR if invalid
    # --------------------------------------------------
    input_validity = validate_input("page1", "table1", t1)

    if not input_validity["total_distance"]: total_distance = ERROR
    if not input_validity["operating_speed"]: operating_speed = ERROR
    if not input_validity["working_days_per_year"]: working_days_per_year = ERROR
    if not input_validity["working_hours_per_day"]: working_hours_per_day = ERROR
    if not input_validity["required_hourly_capacity"]: required_hourly_capacity = ERROR
    if not input_validity["effective_cabin_capacity"]: effective_cabin_capacity = ERROR
    if not input_validity["cabins_per_group"]: cabins_per_group = ERROR
    if not input_validity["acceleration"]: acceleration = ERROR
    if not input_validity["deceleration"]: deceleration = ERROR
    if not input_validity["braking_deceleration"]: braking_deceleration = ERROR
    if not input_validity["creep_speed"]: creep_speed = ERROR
    if not input_validity["creep_distance"]: creep_distance = ERROR

    # --------------------------------------------------
    # 3. Perform calculations
    #    Each output propagates ERROR when any required input is ERROR.
    # --------------------------------------------------

    ########### intermediate calculations ####################

    # acceleration section
    acc = acceleration
    acc_sec_vf = operating_speed
    acc_sec_t = (acc_sec_vf - 0) / acc        # t = (vf-vi)/a, vi=0
    acc_sec_d = 0.5 * (acc_sec_vf + 0) * acc_sec_t  # d=0.5*(vf+vi)*t

    # constant speed section
    const_sec_vf = operating_speed

    # deceleration section
    dec = deceleration
    dec_sec_vf = creep_speed
    dec_sec_t = (dec_sec_vf - const_sec_vf) / dec
    dec_sec_d = 0.5 * (dec_sec_vf + const_sec_vf) * dec_sec_t

    # creep section
    creep_sec_vf = creep_speed
    creep_sec_t = creep_distance / creep_speed
    creep_sec_d = creep_distance

    # braking section
    brake_dec = braking_deceleration
    braking_sec_vf = 0
    braking_sec_t = (braking_sec_vf - creep_sec_vf) / brake_dec
    braking_sec_d = 0.5 * (braking_sec_vf + creep_sec_vf) * braking_sec_t

    # constant speed section (remainder)
    const_sec_d = total_distance - (acc_sec_d + dec_sec_d + creep_sec_d + braking_sec_d)
    const_sec_t = const_sec_d / const_sec_vf

    # total one-way run time and distance
    one_way_run_t = acc_sec_t + const_sec_t + dec_sec_t + creep_sec_t + braking_sec_t
    one_way_run_d = acc_sec_d + const_sec_d + dec_sec_d + creep_sec_d + braking_sec_d

    ########### compute final outputs ####################
    station_dwell_time         = effective_cabin_capacity + 45
    one_way_cycle_time         = station_dwell_time + one_way_run_t
    trips_per_hour             = 3600 / one_way_cycle_time
    hourly_passenger_volume    = trips_per_hour * cabins_per_group * effective_cabin_capacity
    daily_passenger_volume     = hourly_passenger_volume * working_hours_per_day
    annual_passenger_volume    = daily_passenger_volume * working_days_per_year / 10000  # convert to 10k persons

    # --------------------------------------------------
    # 4. Round outputs and return (only one return)
    # --------------------------------------------------

    p1_table2_decimals = 2
    output_data = {}
    output_data["table2"] = _format_table_value(
        {
            "station_dwell_time":         station_dwell_time,
            "one_way_cycle_time":         one_way_cycle_time,
            "trips_per_hour":             trips_per_hour,
            "hourly_passenger_volume":    hourly_passenger_volume,
            "daily_passenger_volume":     daily_passenger_volume,
            "annual_passenger_volume":    annual_passenger_volume,
        },
        p1_table2_decimals,
    )

    # Placeholder for future plot payload separation.
    output_data["plot1"] = {
    "time":     [0, acc_sec_t, const_sec_t, dec_sec_t, creep_sec_t, braking_sec_t],
    "speed":    [0, acc_sec_vf, const_sec_vf, dec_sec_vf, creep_sec_vf, braking_sec_vf],
    }

    return output_data


def compute_page1(page: str, input_data: dict) -> dict:
    """
    Wrapper for page 1 calculations. This is the function registered in the central dispatch.
    It can call multiple internal functions if needed (e.g., separate tables or plots).
    """
    output_data = compute_p1_table(page, input_data)
    return output_data