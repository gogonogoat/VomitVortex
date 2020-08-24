(function(){
function removeModalHide(e){
	this.value.classList.remove("modal_hide");
	this.value.getElementsByClassName('modal_content')[0].scrollTo(0,-99999);
}

function addModalHide(e){
	if(e.target!==e.currentTarget){return;}
	this.value.classList.add("modal_hide");
}
function SetListenerModalBack(){
	Array.from(document.getElementsByClassName('v_note')).forEach((row,index)=>{
		let elm = row.getElementsByClassName('modal_back');
		console.log(Array.from(elm).length);
		if( Array.from(elm).length != 0 ){
			elm[0].addEventListener(
				'click',{
					value:row.getElementsByClassName('modal_back')[0],
					handleEvent:addModalHide
				}
			);
		}
	})
}
function SetListenerModalButton(){
	Array.from(document.getElementsByClassName('v_note')).forEach((row,index)=>{
		let elm = row.getElementsByClassName('btn-push');
		if( Array.from(elm).length != 0 ){
			elm[0].addEventListener(
				'click',{
					value:row.getElementsByClassName('modal_back')[0],
					handleEvent:removeModalHide
				}
			);
		}
	})
}
SetListenerModalBack();
SetListenerModalButton();
})();