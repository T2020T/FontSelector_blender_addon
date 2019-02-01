import bpy
import os

from .properties import FontFolders

addon_name = os.path.basename(os.path.dirname(__file__))

class FontSelectorAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name
    
    # UI
    row_number = bpy.props.IntProperty(
                    default = 5,
                    min = 3,
                    max = 50,
                    description = 'Number of rows by default of the Font List, also the minimum number of row'
                    )
    
    # FONT FOLDERS
    font_folders = bpy.props.CollectionProperty(type = FontFolders)
    
    # PREFS
    prefs_folderpath = bpy.props.StringProperty(
            name = "Preferences Folder Path",
            default = os.path.join(bpy.utils.user_resource('CONFIG'), "font_selector_prefs"),
            description = "Folder where Font Selector Preferences will be stored",
            subtype = "DIR_PATH"
            )

    # PROGRESS BAR
    progress_bar_color = bpy.props.FloatVectorProperty(
            name = "Progress Bar Color", 
            size = 4,
            min = 0.0,
            max = 1.0,
            default = [1, 1, 1, 1],
            subtype = 'COLOR'
            )

    progress_bar_size = bpy.props.IntProperty(
            name = "Progress Bar Size", 
            min = 1,
            max = 100,
            default = 10
            )

    # DEBUG
    debug_value = bpy.props.BoolProperty(
            name = "Debug Toggle", 
            default = False
            )
    
    # STARTUP BEHAVIOR
    startup_check_behavior = bpy.props.EnumProperty(
        name = "Startup Check", 
        default = 'AUTOMATIC_UPDATE',
        items = (
            ('AUTOMATIC_UPDATE', "Auto Update", "Auto Check of Font Folder on startup, if Changes, Blender will refresh the Font List"),
            ('MESSAGE_ONLY', "Message Only", "Auto Check of Font Folder on startup, if Changes, Blender will show a message"),
            ('MANUAL', "Manual", "No Startup Check, Font List has to be manually refreshed"),
            ))
            
    def draw(self, context) :
        layout = self.layout
        font_list = self.font_folders

        temp_list = [f.folderpath for f in font_list]
        
        dupelist = [x for x in temp_list if temp_list.count(x) >= 2]

        col = layout.column(align = True)

        box = col.box()
        row = box.row(align = True)
        row.label(icon = 'SCRIPTWIN')
        row.prop(self, 'prefs_folderpath', text = 'External Preferences Path')
        
        box = col.box()
        row = box.row(align = True)
        row.label(icon = 'BLENDER')
        row.prop(self, 'startup_check_behavior')

        box = col.box()
        row = box.row(align = True)
        row.label("Progress Bar", icon = 'TIME')
        row.prop(self, 'progress_bar_color', text = '')
        row.prop(self, 'progress_bar_size', text = 'Size')
        
        box = col.box()
        row = box.row(align = True)
        row.label('Number of Font list rows', icon = 'COLLAPSEMENU')
        row.prop(self, 'row_number', text = '')
        
        box = col.box()
        row = box.row(align = True)
        row.label("Font Folders", icon = 'FILE_FONT')
        if len(dupelist) > 0 :
            row.label('Dupe Warning', icon = 'ERROR')
        row.operator("fontselector.add_fp", text = "Add Font Folder", icon = 'ZOOMIN')
        row.separator()
        row.operator("fontselector.save_fpprefs", text = 'Save', icon = 'DISK_DRIVE')
        row.operator("fontselector.load_fpprefs", text = 'Load', icon = 'LOAD_FACTORY')
        
        idx = 0
        for i in font_list :
            sub_box = box.box()
            row = sub_box.row()
            row.prop(i, "folderpath")
            if i.folderpath in dupelist:
                row.label(icon = 'ERROR')
            op = row.operator("fontselector.suppress_fp", text = '', icon = 'X', emboss = False)
            op.index = idx
            idx += 1

        box = col.box()
        row = box.row(align = True)
        row.label("Development", icon = 'MOD_SCREW')
        row.prop(self, 'debug_value')
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.user_preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)