using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class ClickToMove : MonoBehaviour {
	// Update is called once per frame
	void Update () {
        if (Input.GetButtonDown("Fire1"))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            int terrainLayerMask=1<<LayerMask.NameToLayer("Terrain");  
            RaycastHit hit;         
            if (Physics.Raycast(ray,out hit,Mathf.Infinity,terrainLayerMask)){
            	// Instantiate(new GameObject(),hit.point,Quaternion.identity);
            	NavMeshAgent agent = GetComponent<NavMeshAgent>();
            	agent.destination = hit.point;
            }
        }
	}
}
