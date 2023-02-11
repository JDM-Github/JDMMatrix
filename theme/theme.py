from dataclasses import dataclass

@dataclass
class AllColor:
    
    WINDOW_BACKGROUND : str
    MAIN_BACKGROUND : str
    MAIN_BG_SOURCE : str
    THEME_FG : str
    THEME_COLOR : str

    BUTTON_LINE : str
    BUTTON_COLOR : str
    BUTTON_FG : str
    BUTTON_PRESSED : str
    
    EXIT_LINE : str
    EXIT_COLOR : str
    EXIT_FG : str
    
    MATRIX_BUTTON_LINE : str
    MATRIX_BUTTON_FG : str
    MATRIX_BUTTON_COLOR : str
    MATRIX_BUTTON_PRESSED : str
    
    MATRIX_ENTRY_COLOR : str
    MATRIX_ENTRY_FG : str
    MATRIX_ENTRY_CURSOR : str
    MATRIX_ENTRY_SELECTION : str
    
    MATRIX_LINE : str
    MATRIX_BOX : str
    
    MENU_COLOR : str
    MENU_BUTTON_COLOR : str
    MENU_BUTTON_PRESSED : str
    
    TITLE_COLOR : str
    ERROR_COLOR : str
    STEP_BY_STEP : str
    NUMBER_COLOR : str
    NORMAL_COLOR : str
    
    FUNC_BUTTON_LINE : str
    FUNC_BUTTON_FG : str
    FUNC_BUTTON_COLOR : str
    FUNC_BUTTON_PRESSED : str
        
    FUNC_ENTRY_SELECTION : str
    FUNC_ENTRY_FG : str
    FUNC_ENTRY_CURSOR : str
    
    RESULT_LINE : str
    RESULT_BOX : str
    
    GRAPH_BG : str
    GRAPH_LINE : str
    GRAPH_NUM_VERT : str
    GRAPH_NUM_HOR : str
    GRAPH_ARROW_ACTIVE : str
    GRAPH_ARROW_NACTIVE : str
    GRAPH_ARROW_TEXT : str
    GRAPH_STATS : str
    
    
    BLACK : str = "000000"
    GRAY : str = "444444"
    LIGHTER_GRAY : str = "888888"
    WHITE : str = "FFFFFF"
    BLUE : str = "0000FF"
    RED : str = "FF0000"
    GREEN : str = "00FF00"

class Theme:
    
    HELLOKITTY : AllColor = AllColor(
        WINDOW_BACKGROUND = "F4F4F5",
        MAIN_BACKGROUND="E5C8D0",
        MAIN_BG_SOURCE="asset/mainBg1.png",
        THEME_FG="F56D93",
        THEME_COLOR = "F4F4F5",

        BUTTON_LINE="FFFFFF",
        BUTTON_FG="FFFFFF",
        BUTTON_COLOR="F56D93",
        BUTTON_PRESSED="F4B3D1",
        
        EXIT_LINE = "FFFFFF" ,
        EXIT_COLOR = "3EcD7F",
        EXIT_FG = "FFFFFF",
        
        MATRIX_BUTTON_LINE="FFFFFF",
        MATRIX_BUTTON_FG ="FFFFFF",
        MATRIX_BUTTON_COLOR="3EcD7F",
        MATRIX_BUTTON_PRESSED="F4B3D1",
        
        MATRIX_ENTRY_COLOR="2EbD6F",
        MATRIX_ENTRY_SELECTION="FFFFFF66",
        MATRIX_ENTRY_FG="FFFFFF",
        MATRIX_ENTRY_CURSOR="FFFFFF",
        
        MATRIX_LINE="FFFFFF",
        MATRIX_BOX="F56D93",
        
        MENU_COLOR = "F4F4F5",
        MENU_BUTTON_COLOR="F56D93",
        MENU_BUTTON_PRESSED="F4B3D1",
        
        TITLE_COLOR="F52077",
        ERROR_COLOR="FF0000",
        STEP_BY_STEP="F56D93",
        NUMBER_COLOR="00FFFE",
        NORMAL_COLOR="FFFFFF",
        
        FUNC_BUTTON_LINE="FFFFFF",
        FUNC_BUTTON_FG="FFFFFF",
        FUNC_BUTTON_COLOR="F56D93",
        FUNC_BUTTON_PRESSED="F4B3D1",
        
        FUNC_ENTRY_SELECTION="FFFFFF66",
        FUNC_ENTRY_FG="FFFFFF",
        FUNC_ENTRY_CURSOR="FFFFFF",
        
        RESULT_LINE="FFFFFF",
        RESULT_BOX="0E9D4F",
        
        GRAPH_BG = "E5C8D0",
        GRAPH_LINE = "F56D93",
        GRAPH_NUM_VERT = "FF6666",
        GRAPH_NUM_HOR = "6666FF",
        GRAPH_ARROW_ACTIVE = "F52077",
        GRAPH_ARROW_NACTIVE = "F56D93",
        GRAPH_ARROW_TEXT = "0E9D4F",
        GRAPH_STATS = "0E9D4F",
    )
    
    ORIGINAL : AllColor = AllColor(
        WINDOW_BACKGROUND = "333333",
        MAIN_BACKGROUND="333333",
        MAIN_BG_SOURCE="asset/mainBg0.png",
        THEME_FG="FFFFFF",
        THEME_COLOR = "000000",

        BUTTON_LINE="FFFFFF",
        BUTTON_FG="FFFFFF",
        BUTTON_COLOR="444444",
        BUTTON_PRESSED="666666",
        
        EXIT_LINE = "FFFFFF" ,
        EXIT_COLOR = "111111",
        EXIT_FG = "FFFFFF",
        
        MATRIX_BUTTON_LINE="FFFFFF",
        MATRIX_BUTTON_FG ="FFFFFF",
        MATRIX_BUTTON_COLOR="444444",
        MATRIX_BUTTON_PRESSED="666666",
        
        MATRIX_ENTRY_COLOR="111111",
        MATRIX_ENTRY_SELECTION="FFFFFF66",
        MATRIX_ENTRY_FG="FFFFFF",
        MATRIX_ENTRY_CURSOR="FFFFFF",
        
        MATRIX_LINE="FFFFFF",
        MATRIX_BOX="444444",
        
        MENU_COLOR = "111111",
        MENU_BUTTON_COLOR="666666",
        MENU_BUTTON_PRESSED="FFFFFF",
        
        TITLE_COLOR="00496c",
        ERROR_COLOR="FF0000",
        STEP_BY_STEP="00FF00",
        NUMBER_COLOR="2596BE",
        NORMAL_COLOR="FFFFFF",
        
        FUNC_BUTTON_LINE="FFFFFF",
        FUNC_BUTTON_FG="FFFFFF",
        FUNC_BUTTON_COLOR="444444",
        FUNC_BUTTON_PRESSED="666666",
        
        FUNC_ENTRY_SELECTION="FFFFFF66",
        FUNC_ENTRY_FG="FFFFFF",
        FUNC_ENTRY_CURSOR="FFFFFF",
        
        RESULT_LINE="FFFFFF",
        RESULT_BOX="111111",
        
        GRAPH_BG = "333333",
        GRAPH_LINE = "000000",
        GRAPH_NUM_VERT = "FF6666",
        GRAPH_NUM_HOR = "6666FF",
        GRAPH_ARROW_ACTIVE = "00ff00",
        GRAPH_ARROW_NACTIVE = "888888",
        GRAPH_ARROW_TEXT = "ffffff",
        GRAPH_STATS = "ffffff",
    )
    JDM : AllColor = AllColor(
        WINDOW_BACKGROUND = "000000",
        MAIN_BACKGROUND="000000",
        MAIN_BG_SOURCE="asset/JDMBG.png",
        THEME_FG="FFFFFF",
        THEME_COLOR = "03d5f5",

        BUTTON_LINE="03d5f5",
        BUTTON_FG="FFFFFF",
        BUTTON_COLOR="000000",
        BUTTON_PRESSED="03d5f5",
        
        EXIT_LINE = "03d5f5" ,
        EXIT_COLOR = "000000",
        EXIT_FG = "FFFFFF",
        
        MATRIX_BUTTON_LINE="03d5f5",
        MATRIX_BUTTON_FG ="FFFFFF",
        MATRIX_BUTTON_COLOR="000000",
        MATRIX_BUTTON_PRESSED="03d5f5",
        
        MATRIX_ENTRY_COLOR="000000",
        MATRIX_ENTRY_SELECTION="FFFFFF66",
        MATRIX_ENTRY_FG="03d5f5",
        MATRIX_ENTRY_CURSOR="03d5f5",
        
        MATRIX_LINE="03d5f5",
        MATRIX_BOX="000000",
        
        MENU_COLOR = "03d5f5",
        MENU_BUTTON_COLOR="FFFFFF",
        MENU_BUTTON_PRESSED="000000",
        
        TITLE_COLOR="03d5f5",
        ERROR_COLOR="FF0000",
        STEP_BY_STEP="311ede",
        NUMBER_COLOR="08fbef",
        NORMAL_COLOR="FFFFFF",
        
        FUNC_BUTTON_LINE="FFFFFF",
        FUNC_BUTTON_FG="FFFFFF",
        FUNC_BUTTON_COLOR="03d5f5",
        FUNC_BUTTON_PRESSED="000000",
        
        FUNC_ENTRY_SELECTION="FFFFFF66",
        FUNC_ENTRY_FG="FFFFFF",
        FUNC_ENTRY_CURSOR="FFFFFF",
        
        RESULT_LINE="03d5f5",
        RESULT_BOX="000000",
        
        GRAPH_BG = "111111",
        GRAPH_LINE = "555555",
        GRAPH_NUM_VERT = "FF6666",
        GRAPH_NUM_HOR = "6666FF",
        GRAPH_ARROW_ACTIVE = "55aaff",
        GRAPH_ARROW_NACTIVE = "888888",
        GRAPH_ARROW_TEXT = "03d5f5",
        GRAPH_STATS = "55aaff",
    )
    GALAXY : AllColor = AllColor(
        WINDOW_BACKGROUND = "333333",
        MAIN_BACKGROUND="333333",
        MAIN_BG_SOURCE="asset/mainBg0.png",
        THEME_FG="FFFFFF",
        THEME_COLOR = "000000",

        BUTTON_LINE="FFFFFF",
        BUTTON_FG="FFFFFF",
        BUTTON_COLOR="444444",
        BUTTON_PRESSED="666666",
        
        EXIT_LINE = "FFFFFF" ,
        EXIT_COLOR = "111111",
        EXIT_FG = "FFFFFF",
        
        MATRIX_BUTTON_LINE="FFFFFF",
        MATRIX_BUTTON_FG ="FFFFFF",
        MATRIX_BUTTON_COLOR="444444",
        MATRIX_BUTTON_PRESSED="666666",
        
        MATRIX_ENTRY_COLOR="111111",
        MATRIX_ENTRY_SELECTION="FFFFFF66",
        MATRIX_ENTRY_FG="FFFFFF",
        MATRIX_ENTRY_CURSOR="FFFFFF",
        
        MATRIX_LINE="FFFFFF",
        MATRIX_BOX="444444",
        
        MENU_COLOR = "111111",
        MENU_BUTTON_COLOR="666666",
        MENU_BUTTON_PRESSED="FFFFFF",
        
        TITLE_COLOR="00496c",
        ERROR_COLOR="FF0000",
        STEP_BY_STEP="00FF00",
        NUMBER_COLOR="2596BE",
        NORMAL_COLOR="FFFFFF",
        
        FUNC_BUTTON_LINE="FFFFFF",
        FUNC_BUTTON_FG="FFFFFF",
        FUNC_BUTTON_COLOR="444444",
        FUNC_BUTTON_PRESSED="666666",
        
        FUNC_ENTRY_SELECTION="FFFFFF66",
        FUNC_ENTRY_FG="FFFFFF",
        FUNC_ENTRY_CURSOR="FFFFFF",
        
        RESULT_LINE="FFFFFF",
        RESULT_BOX="111111",

        GRAPH_BG = "333333",
        GRAPH_LINE = "000000",
        GRAPH_NUM_VERT = "FF6666",
        GRAPH_NUM_HOR = "6666FF",
        GRAPH_ARROW_ACTIVE = "00ff00",
        GRAPH_ARROW_NACTIVE = "888888",
        GRAPH_ARROW_TEXT = "ffffff",
        GRAPH_STATS = "ffffff",
    )
    BLANK : AllColor = AllColor(
        WINDOW_BACKGROUND = "333333",
        MAIN_BACKGROUND="333333",
        MAIN_BG_SOURCE="asset/mainBg0.png",
        THEME_FG="FFFFFF",
        THEME_COLOR = "000000",

        BUTTON_LINE="FFFFFF",
        BUTTON_FG="FFFFFF",
        BUTTON_COLOR="444444",
        BUTTON_PRESSED="666666",
        
        EXIT_LINE = "FFFFFF" ,
        EXIT_COLOR = "111111",
        EXIT_FG = "FFFFFF",
        
        MATRIX_BUTTON_LINE="FFFFFF",
        MATRIX_BUTTON_FG ="FFFFFF",
        MATRIX_BUTTON_COLOR="444444",
        MATRIX_BUTTON_PRESSED="666666",
        
        MATRIX_ENTRY_COLOR="111111",
        MATRIX_ENTRY_SELECTION="FFFFFF66",
        MATRIX_ENTRY_FG="FFFFFF",
        MATRIX_ENTRY_CURSOR="FFFFFF",
        
        MATRIX_LINE="FFFFFF",
        MATRIX_BOX="444444",
        
        MENU_COLOR = "111111",
        MENU_BUTTON_COLOR="666666",
        MENU_BUTTON_PRESSED="FFFFFF",
        
        TITLE_COLOR="00496c",
        ERROR_COLOR="FF0000",
        STEP_BY_STEP="00FF00",
        NUMBER_COLOR="2596BE",
        NORMAL_COLOR="FFFFFF",
        
        FUNC_BUTTON_LINE="FFFFFF",
        FUNC_BUTTON_FG="FFFFFF",
        FUNC_BUTTON_COLOR="444444",
        FUNC_BUTTON_PRESSED="666666",
        
        FUNC_ENTRY_SELECTION="FFFFFF66",
        FUNC_ENTRY_FG="FFFFFF",
        FUNC_ENTRY_CURSOR="FFFFFF",
        
        RESULT_LINE="FFFFFF",
        RESULT_BOX="111111",

        GRAPH_BG = "333333",
        GRAPH_LINE = "000000",
        GRAPH_NUM_VERT = "FF6666",
        GRAPH_NUM_HOR = "6666FF",
        GRAPH_ARROW_ACTIVE = "00ff00",
        GRAPH_ARROW_NACTIVE = "888888",
        GRAPH_ARROW_TEXT = "ffffff",
        GRAPH_STATS = "ffffff",
    )
    CurrentTheme : AllColor = ORIGINAL
