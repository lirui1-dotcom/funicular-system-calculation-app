__all__=['table_texts', 'presets_texts', 'title_texts', 'presets', 'default_language', 
         'menu_texts', 'default_page', 'plot_texts']
# ==========================================================================================
# Language
# ==========================================================================================

default_language = "EN"
supported_languages = ("ZH", "EN")

default_page = "page1"

# ==========================================================================================
# Menu Labels (UI ONLY)
# ==========================================================================================

# ==========================================================================================
# Menu Labels (UI ONLY, CONSISTENT STRUCTURE)
# ==========================================================================================

menu_texts = {

    # menu option 1
    "file": {
        "ZH": "文件",
        "EN": "File",
    },
    "import_excel": {
        "ZH": "导入 Excel…",
        "EN": "Import Excel…",
    },
    "export_excel": {
        "ZH": "导出 Excel…",
        "EN": "Export Excel…",
    },
    "exit": {
        "ZH": "退出",
        "EN": "Exit",
    },
    
    #menu option 2
    "edit": {
        "ZH": "编辑",
        "EN": "Edit",
    },
    "reset": {
        "ZH": "清零",
        "EN": "Reset",
    },

    #menu option 3
    "language": {
        "ZH": "语言",
        "EN": "Language",
    },
}


# ==========================================================================================
# Titles (UI ONLY)
# ==========================================================================================

title_texts= {}
title_texts["main_title"] = {
    "ZH": "客运缆车系统运行参数计算程序",
    "EN": "Passenger Funicular Railway Operating Parameters Calculation Program",
}

title_texts["page1"] = {
    "table1": {
        "ZH": "一   基本参数",
        "EN": "I   Basic Parameters",
    },
    "table2": {
        "ZH": "二   计算结果",
        "EN": "II  Calculation Results",
    },
}



# ==========================================================================================
# Page 1 
# ==========================================================================================

# table 1 fields (KEY = IDENTITY, LABEL = UI)
table_texts={}
table_texts["page1"] = {}
table_texts["page1"]["table1"] = {
    "total_distance": {
        "ZH": "运行总距离(m)",
        "EN": "Total Distance (m)",
    },
    "operating_speed": {
        "ZH": "运行速度(m/s)",
        "EN": "Operating Speed (m/s)",
    },
    "working_days_per_year": {
        "ZH": "年工作天数(d)",
        "EN": "Working Days per Year (d)",
    },
    "working_hours_per_day": {
        "ZH": "日工作小时数(h)",
        "EN": "Working Hours per Day (h)",
    },
    "required_hourly_capacity": {
        "ZH": "要求小时运量(P/h)",
        "EN": "Required Hourly Capacity (persons/h)",
    },
    "effective_cabin_capacity": {
        "ZH": "缆车有效定员(人)",
        "EN": "Effective Cabin Capacity (persons)",
    },
    "cabins_per_group": {
        "ZH": "每组车厢数",
        "EN": "Cabins per Group",
    },
    "acceleration": {
        "ZH": "加速度(m/s²)",
        "EN": "Acceleration (m/s²)",
    },
    "deceleration": {
        "ZH": "减速度(m/s²)",
        "EN": "Deceleration (m/s²)",
    },
    "braking_deceleration": {
        "ZH": "制动段减速度 (m/s²)",
        "EN": "Braking Section Deceleration (m/s²)",
    },
    "creep_speed": {
        "ZH": "爬行速度(m/s)",
        "EN": "Creep Speed (m/s)",
    },
    "creep_distance": {
        "ZH": "爬行距离(m)",
        "EN": "Creep Distance (m)",
    },
}

# Table 2 Fields (OUTPUTS)

table_texts["page1"]["table2"] = {
    "station_dwell_time": {
        "ZH": "上下人及发送信号时间(s)",
        "EN": "Station Dwell Time (s)",
    },
    "one_way_cycle_time": {                    # ← replaced / modernized
        "ZH": "单程运行时间(s)",
        "EN": "One-Way Cycle Time (s)",
    },
    "trips_per_hour": {
        "ZH": "小时运行次数",
        "EN": "Trips per Hour",
    },
    "hourly_passenger_volume": {
        "ZH": "计算小时运量(人/小时)",
        "EN": "Hourly Passenger Volume (pax/h)"
    },
    "daily_passenger_volume": {
        "ZH": "计算日运量(人/天)",
        "EN": "Daily Passenger Volume (pax/day)"
    },
    "annual_passenger_volume": {
        "ZH": "计算年运量(万人/年)",
        "EN": "Annual Passenger Volume (×10k pax)"
}
}

# ==========================================================================================
# Plot texts
# ==========================================================================================
plot_texts = {}
plot_texts["page1"] = {}
plot_texts["page1"]["plot1"] = {

    "title": {
        "ZH": "速度梯形图",
        "EN": "Speed Profile",
    },
    "x_label": {
        "ZH": "运行时间 (s)",
        "EN": "Operating time (s)",
    },
    "y_label": {
        "ZH": "运行速度 (m/s)",
        "EN": "Operating Speed (m/s)",
    },
    "no_input_error_message": {
        "ZH": "请输入必要参数以预览图表",
        "EN": "Please enter required parameters to preview chart",
    },
    "invalid_input_error_message": {
        "ZH": "输入参数无效，请检查参数并重试",
        "EN": "Preview unavailable due to invalid inputs",
    },
}


# ==========================================================================================
# Presets
# (KEYS MUST MATCH FIELD KEYS — NEVER UI LABELS)
# ==========================================================================================

presets_texts = {
    # presets label text
    "label_text": {
        "ZH": "参考项目",
        "EN": "Presets",
    },

    # first drop down text
    "default_option": {
        "ZH": "手动输入",
        "EN": "Manual Input",
    },        
}

presets = {}
presets["page1"] = {}
presets["page1"]["table1"] = {}
presets["page1"]["table1"]["opt1"] = {
            "texts": {
                "ZH": "参考项目 1",
                "EN": "Sample 1",
            },
            "data": {
                "total_distance": "90.46960781",
                "operating_speed": "1.5",
                "working_days_per_year": "300",
                "working_hours_per_day": "8",
                "required_hourly_capacity": "600",
                "effective_cabin_capacity": "121",
                "cabins_per_group": "1",
                "acceleration": "0.25",
                "deceleration": "-0.25",
                "braking_deceleration": "-0.1",
                "creep_speed": "0.1",
                "creep_distance": "0.5",
            },          
}


