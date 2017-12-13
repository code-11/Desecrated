using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MainMenu : MonoBehaviour {
	public Button lvlOne;
    void Start()
    {
        lvlOne.onClick.AddListener(onLvlOneClick);
    }

    void onLvlOneClick()
    {
        Debug.Log("You have clicked the button!");
    }
}
