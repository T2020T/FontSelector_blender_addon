import bpy
import os

from ..functions.check_size import check_size_changes
from ..functions.check_desync_fonts import checkDesyncFonts
from ..preferences import get_addon_preferences
from ..functions.misc_functions import absolute_path

from ..global_variable import json_file
from ..global_messages import *

class FontSelectorCheckChanges(bpy.types.Operator):
    bl_idname = "fontselector.check_changes"
    bl_label = "Check Changes"
    bl_description = "Check for changes in Font Folders"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        json = os.path.join(prefs, json_file)
        return prefs!="" and os.path.isfile(json)
    
    def execute(self, context):
        # font folders
        chk_changes = check_size_changes()

        if chk_changes :
            bpy.ops.fontselector.dialog_message('INVOKE_DEFAULT', code = 1)
            
        else :
            self.report({'INFO'}, no_changes_msg)
            print(print_statement + no_changes_msg)

        # font objects
        checkDesyncFonts()
    
        return {'FINISHED'}