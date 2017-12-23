using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Farmer : MonoBehaviour, IProfession {
	public string getName(){
		return "Farmer";
	}
	
	public string provideActivity(){
		int choice= Random.Range(0,3);
		if (choice==0){
			return "Field";
		}else if (choice==1){
			return "Shed";
		}else if (choice==2){
			return "House";
		}else{
			return "Broken";
		}
	}
}
