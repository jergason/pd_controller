package  {
	
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Point;
	
	public class Tank extends MovieClip{

		//between -1 and 1
		public var angularVelocity:Number=0;
		public var velocity:Number=0;
		
		//vector components for velocity
		private var xSpeed:Number=0;
		private var ySpeed:Number=0;
		
		private var maxSpeed:Number = 7;
		private var maxAngle:Number = 10;
		
		private var fieldsApplied:Boolean = false;
				
		private var goal:FieldObject;
		private var walls:Walls;
		
		
		public function Tank() {			
			addEventListener(Event.ADDED_TO_STAGE, added);
		}
		
		
		private function added(e:Event):void {
			walls = PotentialFields.getInstance().getWalls();;
			goal = PotentialFields.getInstance().getGoal();
			addEventListener(Event.ENTER_FRAME, moveTank);
			addEventListener(MouseEvent.MOUSE_DOWN, selectTank);			
		}
		
		
		private function moveTank(e:Event):void{
			
			if(fieldsApplied){
				var goalDx = this.x - goal.x;
				var goalDy = this.y - goal.y;
				var goalDist = Math.sqrt(goalDx * goalDx + goalDy * goalDy);
				velocity = goalDist / 50;
				if (velocity > 1) {
					velocity = 1;
				}
				
				fieldAdjustments();
				
			}
			
			
			this.rotation+=angularVelocity*maxAngle;
			xSpeed = velocity*Math.cos(this.rotation*Math.PI/180)*maxSpeed;
			ySpeed = velocity*Math.sin(this.rotation*Math.PI/180)*maxSpeed;
			if(!walls.hitTestPoint(x+xSpeed,y,true)){
				x += xSpeed;
			}
			
			if(!walls.hitTestPoint(x,y+ySpeed,true)){
				y += ySpeed;
			}
			
		}
		
		public function applyFields():void{
			fieldsApplied=true;
		}
		
		public function disableFields():void{
			fieldsApplied=false;
			velocity=0;
			angularVelocity=0;
		}
		
		public function getFieldsApplied():Boolean{
			return fieldsApplied;
		}
		
		private function fieldAdjustments():void{
			var deltaX:Number=0;
			var deltaY:Number=0;
			
			var myPoint:Point = new Point(this.x, this.y);
			var components:Point = PotentialFields.getInstance().computeVectorComponents(myPoint);
			
			
			var targetAngle:Number = Math.atan2(components.y,components.x)*180/Math.PI;
			
			//adjust angle velocity based on target angle
			var myAngle:Number = (this.rotation+360)%360;
			targetAngle = (targetAngle+360)%360


			var angleMagnitude:Number = Math.abs(myAngle-targetAngle)/maxAngle;
			var scaleAngle:Number;
			if(angleMagnitude<1){
				scaleAngle = angleMagnitude;
			}
			else{
				scaleAngle = 1;
			}
						
			angularVelocity = scaleAngle*determineAngleDirection(myAngle,targetAngle);

		}
	
		
		private function determineAngleDirection(myAngle:Number,targetAngle:Number):int{
			var deltaCW:Number=0;
			var deltaCCW:Number = 0;
			var deltaStep:Number = .1;
			var errorRange:Number = .5;
			
			var tempAngle:Number = myAngle;
			
			//sweep CCW
			while(  Math.abs(tempAngle-targetAngle)>errorRange){
				tempAngle +=deltaStep;
				deltaCCW += deltaStep;
				if(tempAngle>360){
					tempAngle-=360;
				}
			}
			
			tempAngle = myAngle;
			
			//sweep CW
			while(  Math.abs(tempAngle-targetAngle)>errorRange){
				tempAngle -=deltaStep;
				deltaCW += deltaStep;
				if(tempAngle<0){
					tempAngle+=360;
				}
			}
			
			if(deltaCW <= deltaCCW){
				return -1; //go CW
			}
			return 1; //go CCW
			
		}
		
		private function selectTank(e:Event):void{
			dispatchEvent(new Event("selectTank"));
		}
		
		public function setAngularVelocity(angVel:Number){
			angularVelocity = angVel;
		}
		
		public function setVelocity(vel:Number):void{
			velocity = vel;
		}
		
		public function getAngleVel():Number{
			return angularVelocity;
		}
		
		public function getVel():Number{
			return velocity;
		}
		
	

	}
	
}
