using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour {
	public Button lvlOneBtn;
    void Start()
    {
        lvlOneBtn.onClick.AddListener(onLvlOneClick);
    }

    void onLvlOneClick()
    {
        SceneManager.LoadScene(Globals.LevelOne, LoadSceneMode.Single);
    }
}
