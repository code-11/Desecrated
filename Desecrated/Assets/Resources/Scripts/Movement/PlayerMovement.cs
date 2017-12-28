using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour {

	public float speed=100.0f;	
	public float radius=.2f;
	public bool debug=false;

	// Update is called once per frame
	void Update () {
		float xMov = Input.GetAxisRaw("Horizontal");
		float zMov = Input.GetAxisRaw("Vertical");
		float x=transform.position.x;
		float y=transform.position.y;
		float z=transform.position.z;
		Vector3 movDelta= new Vector3(xMov,0,zMov);
		movDelta.Normalize();
		movDelta*=speed;
		movDelta*=Time.deltaTime;
		Vector3 newPos=new Vector3(x+movDelta.x,y,z+movDelta.z);
		int buildingMask=(1<<LayerMask.NameToLayer("Buildings"));
		Collider[] colliders=Physics.OverlapSphere(newPos,radius,buildingMask);
		if (colliders.Length==0){
			transform.Translate(movDelta);
		}else{
			Debug.Log(colliders[0].name);
		}
	}
}
