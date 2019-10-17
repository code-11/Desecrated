open Printf;;

type concept = Death 
			| Fire  
			| Decay 
			| Restoration 
			| Knowledge 
			| Magic 
			| Holy 
			| Life 
			| Wealth;;

type body_part = Brow
			| Arm
			| Leg
			| Torso
			| Head
			| Finger
			| Toe
			| Heel
			| Ankle
			| Thigh
			| Shin
			| Skin
			| Heart
			| Lungs
			| Eye
			| Ear
			| Lips
			| Hair
			| Stomach;;

type god = string * (concept list);;

type action = string * (concept list);;

type ur_action = string * (action list) * (concept list);;

type item = string * (ur_action list) * (concept list);;

let average a b =
  (a +. b) /. 2.0;;
let (melted:action) = ("Melted",[Fire]);;
let (destroy:ur_action) = ("Destroy",[melted],[Death]);;
let (forged:action) = ("Forged",[Life]);;
let (create:ur_action) = ("Create",[forged],[Life]);;
let (necklace:item) = ("Necklace",[create; destroy],[Wealth]);;

Printf.printf "%.3f" (average 5.0 10.0)