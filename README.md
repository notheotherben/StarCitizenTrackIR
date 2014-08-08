# Setting up TrackIR for StarCitizen
This guide will attempt to get you on the right track for configuring TrackIR to
run in StarCitizen (in its current state).

First, a quick introduction to what TrackIR is, and how it's supposed to work.
TrackIR is an optical head-tracking solution developed by NaturalPoint to help
improve immersion in games and give you a tactical advantage in combat by allowing
you to rapidly and accurately adjust your perspective independent of your direction
of aim.

As you can no doubt imagine, this gives you a massive advantage over players who
have to resort to using either POV switches (which are irritatingly slow) or their
mouse (which often prevents them from manouvering simultaneously).

In most cases, TrackIR is something which needs to be integrated by the developer,
but luckily for us RSI have included all the required functionality as part of their
game. All we need to do is get TrackIR input into a form that StarCitizen recognizes.

We're going to be using FreePIE for this in combination with vJoy, the intention
is to allow us to emulate a second joystick which reports the TrackIR pitch and yaw
axes. If this sounds scary, basically we're making your computer think that the TrackIR
is a joystick.

## Required Tools
 - [Joy](http://vjoystick.sourceforge.net/site/)
 - [FreePIE](http://andersmalmgren.github.io/FreePIE/)

Once you've installed both of those programs, you'll need to open up the vJoy configuration
program ("Configure vjoy" in your start menu) and make sure that only X, Y and Z are checked,
set the number of buttons and number of POVs to zero.

Once that's done, you might be asked to restart your computer - please do so before
continuing or you're likely to experience errors.

## The Script
The next step is to load up a script within FreePIE which handles the mapping.
You can use the one below, or write your own if you wish.

```python
import sys

def toIntSafe(value):
    if value > sys.maxint: return sys.maxint
    if value < -sys.maxint: return -sys.maxint
    return value

def update():
	yaw = filters.mapRange(trackIR.yaw, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
	pitch = filters.mapRange(trackIR.pitch, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
	roll = filters.mapRange(trackIR.roll, -50, 50, -vJoy[0].axisMax, vJoy[0].axisMax)

	vJoy[0].x = toIntSafe(yaw)
	vJoy[0].y = toIntSafe(pitch)
	vJoy[0].z = toIntSafe(roll)

if starting:
    trackIR.update += update
```

At this point you should be able to check that the X, Y and Z TrackIR axes are
mapped correctly to vJoy by running the script and opening up "Monitor vjoy".
Alternatively you can `Win + R` *joy.cpl* to open up the Windows joystick dialog
and monitor it from there.

If you get an error when running the script which looks like
"Axis HID_USAGE_X not enabled..." and you're absolutely certain you configured vJoy
correctly then what's probably happened is that FreePIE's version of the vJoy interface
is out of date. Take a look at the [Fixes](#fixes) section for more details.

## StarCitizen's ActionMap
The final step is to actually bind your vJoy virtual joystick to your view controls,
this is done by modifying your ActionMap key bindings to include them. You can find
your layouts in **%StarCitizen%\CitizenClient\Data\Controls\Mappings**, and you
just need to merge the following into your XML.

My recommendation is to create a **layout_trackir.xml** file and drop the following
stuff into it, Star Citizen's action maps are applied progressively - so you can
load your joystick one up and then load the TrackIR setup without any issues.

Once that's done, open up StarCitizen and once you're in Arena Commander run
`pp_rebindkeys layout_trackir` from the console.

```xml
<ActionMaps version="0">
	<actionmap name="spaceship_view">
		<action name="v_view_yaw">
			<rebind device="joystick" input="js2_x" />
		</action>
		<action name="v_view_pitch">
			<rebind device="joystick" input="js2_y" />
		</action>
		<action name="v_view_roll_absolute">
			<rebind device="joystick" input="js2_z" />
		</action>
	</actionmap>
</ActionMaps>
```

## Fixes
### Axis HID_USAGE_X not enabled
This issue is commonly caused by FreePIE's vJoy interface being out of date, you
can solve it by downloading the latest [vJoy SDK](http://sourceforge.net/projects/vjoystick/files/Beta%202.x/2.0.4%20080714/vJoy204SDK-080714.zip/download)
and extracting the **c#/x86/vJoyInterface.dll** file into your **C:\Program Files (x86)\FreePIE** directory.

Once you've extracted the DLL make sure that you right click, select properties and unblock it
or you'll probably be unable to start FreePIE (due to .NET's security features for remote DLLs).

I've submitted a pull request on the FreePIE GitHub project which addresses this
issue, and it's been merged, so with any luck the next version won't have this issue.
