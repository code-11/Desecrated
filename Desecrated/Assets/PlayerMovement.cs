using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour {

	public float speed=100.0f;	

	// Update is called once per frame
	void Update () {
		float xMov = Input.GetAxisRaw("Horizontal");
		float yMov = Input.GetAxisRaw("Vertical");
		float x=transform.position.x;
		float y=transform.position.y;
		float z=transform.position.z;
		Vector2 movDelta= new Vector2(xMov,yMov);
		movDelta.Normalize();
		movDelta*=speed;
		movDelta*=Time.deltaTime;
		float radius=.155f;
		Vector2 newPos=new Vector2(x+movDelta.x,y+movDelta.y);
		Collider2D collider=Physics2D.OverlapCircle(newPos,radius);
		if (collider==null){
			transform.Translate(movDelta);
		}
	}
}
