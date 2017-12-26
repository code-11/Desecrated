using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour {

	public float speed=100.0f;	

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
		float radius=.1f;
		Vector3 newPos=new Vector3(x+movDelta.x,0,z+movDelta.z);
		Collider[] colliders=Physics.OverlapSphere(newPos,radius);
		if (colliders.Length==0){
			transform.Translate(movDelta);
		}
	}
}
