function tabSignal()
{return tabSignal;}
tabSignal.slotArray=new Array();tabSignal.debug=false;tabSignal.sigId=1000000;tabSignal.connect=function(slot_name,signal_name,slot_function,priority=undefined)
{if(slot_function===undefined)
{slot_function=signal_name;signal_name=slot_name;slot_name="sig"+(tabSignal.sigId++)}
return tabSignal.on({signal:signal_name,slot:slot_name,function:slot_function,priority:priority,})}
tabSignal.on=function(callobj)
{if(!callobj.slot)
{callobj.slot="sig"+(tabSignal.sigId++)}
if(callobj.priority===undefined)
{callobj.priority=tabSignal.sigId}
if(tabSignal.slotArray[callobj.signal]===undefined)
{tabSignal.slotArray[callobj.signal]=[]}
tabSignal.slotArray[callobj.signal].push({function:callobj.function,slot:callobj.slot,priority:callobj.priority,once:callobj.once})
if(tabSignal.slotArray[callobj.signal].length)
{tabSignal.slotArray[callobj.signal].sort((a,b)=>{let res=a.priority-b.priority
if(isNaN(res))
{return 0}
return res})}
return callobj.slot;}
tabSignal.once=function(signal_name,slot_function)
{return tabSignal.on({signal:signal_name,slot:"sig"+(tabSignal.sigId++),function:slot_function,priority:(tabSignal.sigId++),once:true,})}
tabSignal.disconnect=function(slot_name,signal_name)
{if(tabSignal.slotArray[signal_name]!==undefined)
{for(let i in tabSignal.slotArray[signal_name])
{let val=tabSignal.slotArray[signal_name][i];if(val.slot==slot_name)
{tabSignal.slotArray[signal_name].splice(i,1)
return true}}}
return false}
tabSignal.emit=function(signal_name,param,SignalNotFromThisTab=false,failed=false)
{if(tabSignal.slotArray[signal_name]===undefined)
{if(tabSignal.debug)console.log("На сигнал "+signal_name+" нет подписчиков")}
else
{if(tabSignal.debug)console.log("Сигнал "+signal_name+" подписаны слоты")
let obj=tabSignal.slotArray[signal_name].slice();let onceIds=[]
for(let i in obj)
{if(obj.hasOwnProperty(i)&&obj[i]!==undefined)
{if(obj[i].once)
{onceIds.push(i)}
if(window.isDebug||!failed)
{obj[i].function(param,signal_name,SignalNotFromThisTab===true,obj[i].slot)}
else
{try{obj[i].function(param,signal_name,SignalNotFromThisTab===true,obj[i].slot)}catch(exception){console.warn("Error in emit signal "+signal_name,exception)}}}}
for(let i in onceIds)
{tabSignal.slotArray[signal_name].splice(onceIds[i],1)}}}
tabSignal.emitAll=function(signal_name,param)
{tabSignal.emit(signal_name,param)
try{if(window['localStorage']!==undefined)
{var curent_custom_id=Math.random()+"_"+Math.random()+"_"+Math.random()+"_"+Math.random()+"_"+Math.random()
window['localStorage']['tabSignal_storage_emit']=JSON.stringify({name:signal_name,custom_id:curent_custom_id,param:param});}
return true}catch(e){return false}}
if(!tabSignal.init)
{tabSignal.init=true
if(window.addEventListener)
{window.addEventListener('storage',function(e)
{if(e.key&&e.key=='tabSignal_storage_emit')
{try{var data=JSON.parse(e.newValue);if(data!==undefined&&data.name!==undefined)
{if(tabSignal.debug>1)console.log(data)
tabSignal.emit(data.name,data.param,true)}}
catch(failed)
{}}},false);}
else
{document.attachEvent('onstorage',function(e)
{if(e.key&&e.key=='tabSignal_storage_emit')
{try{var data=JSON.parse(e.newValue);if(data!==undefined&&data.name!==undefined)
{if(tabSignal.debug>1)console.log(data)
tabSignal.emit(data.name,data.param,true)}}
catch(failed)
{}}});}}