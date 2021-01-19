from dragonfly import (Grammar, CompoundRule, AppContext, FuncContext,
                       MappingRule, Function, PlaySound)

sound_path = "C:\\Users\\Daniel\\DragonSounds\\mmbn\\"
sounds = {
	"refresh": sound_path + "refresh.wav",
	"error": sound_path + "error.wav",
	"shift": sound_path + "shift.wav",
	"revert": sound_path + "revert.wav",

	"yank": sound_path + "yank.wav",
	"paste": sound_path + "paste.wav",
	"delete": sound_path + "delete.wav",
	"blip": sound_path + "blip.wav",

	"write": sound_path + "write.wav",

	"mode imm": sound_path + "mode-imm.wav",
	"mode cmd": sound_path + "mode-cmd.wav",
	"mode vis": sound_path + "mode-vis.wav",
}
def play_sound(name):
	PlaySound(file=sounds[name]).execute()
def make_sound_action(name):
	return PlaySound(file=sounds[name])
