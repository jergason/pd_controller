package 
{
	import flash.display.DisplayObject;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Point;
	
	/**
	 * ...
	 * @author Kason McEwen
	 */
	public class PotentialFields extends MovieClip
	{
		private var vectors:Array = [];
		private var attractiveFlds:Array = [];
		private var repulsiveFlds:Array = [];
		private var tangentFlds:Array = [];
		
		private static var instance:PotentialFields;
		
		private var tanks:Array = [];
		private var addItemsPanel:AddItemsPanel;
		
		private var walls:Walls;
		
		public function PotentialFields() {
			instance = this;
			addItemsPanel = addItemsPanelInstance;
			walls = wallsInstance;
			
			for (var i:int = 0; i < stage.stageWidth; i += 13) {
				for (var j:int = 0; j < stage.stageHeight; j += 13) {
					var vector:VectorLine = new VectorLine();					
					vector.x = i;
					vector.y = j;
					addChild(vector);
					vectors.push(vector);			
				}
			}
			
			for (var k:int = 0; k < numChildren; k++) {
				
				if (getChildAt(k) is AttractiveField) {
					attractiveFlds.push(getChildAt(k));
				}
				if (getChildAt(k) is RepulsiveField) {
					repulsiveFlds.push(getChildAt(k));
				}
				if (getChildAt(k) is TangentialField) {
					tangentFlds.push(getChildAt(k));
				}
				
			}
			
			var allFlds:Array = [].concat(tangentFlds).concat(repulsiveFlds).concat(attractiveFlds);
			for each(var fldObj:FieldObject in allFlds) {
				addChild(fldObj);
			}
			
			addEventListener(Event.ENTER_FRAME, moveVectors);
			
			addItemsPanel.addEventListener("addTank", addTank);
			addItemsPanel.addEventListener("addRepulsive", addRepulsiveFld);
			addItemsPanel.addEventListener("addTangential", addTangentialFld);
			addItemsPanel.addEventListener("randomizeTanks", randomizeTanks);
			addItemsPanel.addEventListener("addWall", addWallMode);
			addChild(addItemsPanel);
		}
		
		
		public function hideVectors(e:Event):void {
			for each(var vector:VectorLine in vectors) {
				vector.visible = false;
			}
		}
		
		public function showVectors(e:Event):void {
			for each(var vector:VectorLine in vectors) {
				vector.visible = true;
			}
		}
		
		private function addWallMode(e:Event):void {
			walls.addWallMode();
		}
		
		private function addTank(e:Event):void {
			var tank:Tank = new Tank();
			addRandomLocation(tank);
			tanks.push(tank);
			tank.applyFields();
		}
		
		private function addRepulsiveFld(e:Event):void {
			var repulsiveFld:RepulsiveField = new RepulsiveField();
			addRandomLocation(repulsiveFld);
			repulsiveFlds.push(repulsiveFld);
		}
		
		private function addTangentialFld(e:Event):void {
			var tangentialFld:TangentialField = new TangentialField();
			addRandomLocation(tangentialFld);
			tangentFlds.push(tangentialFld);
		}
		
		private function randomizeTanks(e:Event):void {
			for each(var tank in tanks) {
				addRandomLocation(tank);
			}
		}
		
		private function addRandomLocation(obj:DisplayObject) {
			obj.x = 200 + Math.random() * (stage.stageWidth - 400);
			obj.y = 100 + Math.random() * (stage.stageHeight - 200);
			addChild(obj);
		}
		
		
		public static function getInstance():PotentialFields {
			return instance;
		}
		
		private function moveVectors(e:Event):void {

			for each(var vector:VectorLine in vectors) {
				var vectorComponents:Point = computeVectorComponents(new Point(vector.x,vector.y));
				vector.setComponents(vectorComponents.x, vectorComponents.y);
			}
		}

		public function getWalls():Walls {
			return walls;
		}
		
		//takes in a point (x,y) and returns vector components based on attractive, repulsive and tangential field objects
		public function computeVectorComponents(pt:Point):Point
		{
			
			var alpha:Number = 500; //attractive constant
			var beta:Number = 5000; //repulsive
			var gamma:Number = 4000; //tanent
			var dx:Number = 0;
			var dy:Number = 0;
				
				for each(var attractiveFld:AttractiveField in attractiveFlds) {
					var dxAttract = attractiveFld.x - pt.x;
					var dyAttract = attractiveFld.y - pt.y;
					var distAttract:Number = Math.sqrt(dxAttract * dxAttract + dyAttract * dyAttract);
					dx += alpha*dxAttract/distAttract;
					dy += alpha*dyAttract/distAttract;
					
				}
				
				
				for each(var repulsiveFld:RepulsiveField in repulsiveFlds) {
					var radiusAffect:Number = repulsiveFld.getRadius();
					var dxRepulse = repulsiveFld.x - pt.x;
					var dyRepulse = repulsiveFld.y - pt.y;
					var distRepulse:Number = Math.sqrt(dxRepulse * dxRepulse + dyRepulse * dyRepulse);
					
					if(distRepulse<radiusAffect){
						dx -= beta * dxRepulse/Math.pow(distRepulse,1.4);
						dy -= beta * dyRepulse / Math.pow(distRepulse, 1.4);
					}
					
				}
				
				//for tangential fields we will want to get a perpindicular vector
				//so dx=dy & dy=-dx -- this creates a clock wise tangential field
				for each(var tangentFld:TangentialField in tangentFlds) {
					
					var radiusAffectTangent:Number = tangentFld.getRadius();
					var dxTangent = (tangentFld.y -pt.y); //dy
					var dyTangent  = -(tangentFld.x - pt.x); //-dx
					
					
					var distTangent:Number = Math.sqrt(dxTangent * dxTangent + dyTangent * dyTangent);
					
					if(distTangent<radiusAffectTangent){
						dx += gamma * dxTangent/Math.pow(distTangent,1);
						dy += gamma * dyTangent / Math.pow(distTangent, 1);
					}
					
				}
				
				return new Point(dx, dy);
		}
		
		public function getGoal() {
			return goalFld;
		}
	
		
	}
	
}