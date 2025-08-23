# %name%

## What is %name%?

%name% (%name_shorthand%) is aimed to provide a management solution to
custom properties in Blender. By default, Blender does not provide a way for
users or add-on/extension authors to group related custom properties in the
UI. %name% solves this by visually separating groups using
UI sub-panels. Properties can be edited to change groups and both groups and
properties can be rearranged. A button is also added to add a new group
manually.

## Installation

1. Download the .zip archive from releases.
   > DO NOT unzip the archive! Blender uses .zip archives to install add-ons
   > and extensions.
2. Place the downloaded archive wherever you store external Blender
   add-ons/extensions.
3. In Blender, go to Edit -> Preferences -> Add-ons.
4. Click dropdown menu and select "Install from Disk..."
   > The dropdown menu is denoted with an upsidedown caret symbol (v)
5. Navigate to your previously downloaded archive, select it, and then click
   "Install from Disk".

## Key Features

### *From User Perspective*

* Automatically adds grouping functionality to all custom properties
* Adds UI ability to rearrange custom properties both inside and outside of
  groups
* Adds button to create custom property groups in the UI

### *From Scripting Perspective*

* (WIP) - Links original custom property references to the newly formed
  %name_shorthand% properties, allowing for updates of the original property
  to be reflected in %name_shorthand%'s properties.

## Quick Reference

