"Resource/UI/HudDamageAccount.res"
{
	"CDamageAccountPanel"
	{
		"fieldName"				"CDamageAccountPanel"
		"text_x"				"0"
		"text_y"				"0"
		"delta_item_end_y"		"0"
		"PositiveColor"         "0 255 0 255"
		"NegativeColor"         "255 0 0 255"
		"delta_lifetime"		"3.2"
		"delta_item_font"		"HudFontMediumBold"
		"delta_item_font_big"	"HudFontMediumBold"
		"EventColor"            "0 255 0 255"
	}
	
	"DamageAccountValue"
	{
		"ControlName"	"CExLabel"
		"accumulative_deltas" "1"
		"fieldName"		"DamageAccountValue"
		"ypos"			"c+111"
		"xpos"			"c-9"
		"zpos"			"2"
		"wide"			"100"
		"tall"			"26"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"%metal%"
		"textAlignment"	"west"
		"fgcolor"		"255 255 0 255"
		"font"			"HudFontMediumSmallBold"
	}
	
	"DamageAccountValueBG"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"DamageAccountValue"
		"xpos"			"c-10"
		"ypos"			"c+110"
		"zpos"			"1"
		"wide"			"100"
		"tall"			"26"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"%metal%"
		"textAlignment"	"west"
		"fgcolor"		"0 0 0 255"
		"font"			"HudFontMediumSmallBold"
	}
}	