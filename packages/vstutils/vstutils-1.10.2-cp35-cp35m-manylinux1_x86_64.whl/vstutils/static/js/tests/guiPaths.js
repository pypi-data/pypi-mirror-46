function rundomString(length,abc="qwertyuiopasdfghjklzxcvbnm012364489")
{let res=""
for(let i=0;i<length;i++)
{res+=abc[Math.floor(Math.random()*abc.length)]}
return res;}
guiLocalSettings.setAsTmp('page_update_interval',600)
guiLocalSettings.get('guiApi.real_query_timeout',1200)
guiTests={}
guiTests.openPage=function(test_name,env,path_callback)
{syncQUnit.addTest("guiPaths['"+test_name+"']",function(assert)
{let path;if(env===undefined)
{path=test_name}
else if(typeof env=="string")
{path=env}
else
{path=path_callback(env);}
let done=assert.async();$.when(vstGO(path)).done(()=>{assert.ok(true,'guiPaths["'+path+'"].opened');testdone(done)}).fail(()=>{debugger;assert.ok(false,'guiPaths["'+path+'"].opened openPage=fail');testdone(done)})});}
guiTests.wait=function(test_name,time=undefined)
{if(!time)
{time=guiLocalSettings.get('page_update_interval')*2.2}
syncQUnit.addTest("wait['"+test_name+"']",function(assert)
{let done=assert.async();setTimeout(()=>{assert.ok(true,'wait["'+test_name+'"]');testdone(done)},time)});}
guiTests.openError404Page=function(env,path_callback)
{syncQUnit.addTest("guiPaths['openError404Page'].Error404",function(assert)
{let done=assert.async();let path=path_callback(env);$.when(vstGO(path)).always(()=>{assert.ok($(".error-as-page.error-status-404").length!=0,'guiPaths["'+path+'"] ok, and delete was failed');testdone(done)})})}
guiTests.createObject=function(path,fieldsData,env={},isWillCreated=true)
{guiTests.openPage(path+"new")
guiTests.setValuesAndCreate(path,fieldsData,(data)=>{if(data.id)
{env.objectId=data.id;}
else if(data.pk)
{env.objectId=data.pk;}
else if(data.name)
{env.objectId=data.name;}},isWillCreated)}
guiTests.setValuesAndCreate=function(path,fieldsData,onCreateCallback,isWillCreated=true)
{syncQUnit.addTest("guiPaths['"+path+"'] WillCreated = "+isWillCreated+", fieldsData="+JSON.stringify(fieldsData),function(assert)
{let done=assert.async();if(typeof fieldsData=="function"){fieldsData=fieldsData();}
let values=guiTests.setValues(assert,fieldsData)
$.when(window.curentPageObject.createAndGoEdit()).done(()=>{assert.ok(isWillCreated==true,'guiPaths["'+path+'"] done');guiTests.compareValues(assert,path,fieldsData,values)
onCreateCallback(window.curentPageObject.model.data)
testdone(done)}).fail((err)=>{assert.ok(isWillCreated==false,'guiPaths["'+path+'"] setValuesAndCreate=fail');testdone(done)})});}
guiTests.updateObject=function(path,fieldsData,isWillSaved=true)
{syncQUnit.addTest("guiPaths['"+path+"update'] isWillSaved = "+isWillSaved+", fieldsData="+JSON.stringify(fieldsData),function(assert)
{let done=assert.async();if(typeof fieldsData=="function"){fieldsData=fieldsData();}
let values=guiTests.setValues(assert,fieldsData)
$.when(window.curentPageObject.update()).done(()=>{assert.ok(isWillSaved==true,'guiPaths["'+path+'update"] done');guiTests.compareValues(assert,path,fieldsData,values)
testdone(done)}).fail((err)=>{if(isWillSaved!=false)debugger;assert.ok(isWillSaved==false,'guiPaths["'+path+'update"] updateObject=fail');testdone(done)})});}
guiTests.compareValues=function(assert,path,fieldsData,values)
{for(let i in fieldsData)
{let field=window.curentPageObject.model.guiFields[i]
if(fieldsData[i].do_not_compare)
{continue;}
assert.ok(field,'test["'+path+'"]["'+i+'"] exist');try{assert.ok(field.getValue()==values[i],'test["'+path+'"]["'+i+'"] == '+values[i]);}catch(e){}}}
guiTests.setValues=function(assert,fieldsData)
{let values=[]
for(let i in fieldsData)
{let field=window.curentPageObject.model.guiFields[i]
values[i]=field.insertTestValue(fieldsData[i].value)
if(fieldsData[i].real_value!=undefined&&values[i]!=fieldsData[i].real_value)
{debugger;assert.ok(false,'fieldsData["'+i+'"].real_value !='+values[i]);}}
return values}
guiTests.actionAndWaitRedirect=function(test_name,assert,action)
{var def=new $.Deferred();let timeId=setTimeout(()=>{assert.ok(false,'actionAndWaitRedirect["'+test_name+'"] and redirect faild');def.reject();},30*1000)
tabSignal.once("spajs.opened",()=>{clearTimeout(timeId)
assert.ok(true,'actionAndWaitRedirect["'+test_name+'"] and redirect');def.resolve();})
action(test_name)
return def.promise();}
guiTests.testActionAndWaitRedirect=function(test_name,action)
{syncQUnit.addTest("testActionAndWaitRedirect['"+test_name+"']",function(assert)
{let done=assert.async();$.when(guiTests.actionAndWaitRedirect(test_name,assert,action)).always(()=>{testdone(done)})});}
guiTests.clickAndWaitRedirect=function(secector_string)
{guiTests.testActionAndWaitRedirect("click for "+secector_string,()=>{$(secector_string).trigger('click')})}
guiTests.deleteObject=function()
{guiTests.clickAndWaitRedirect(".btn-delete-one-entity")}
guiTests.deleteObjByPath=function(path,env,pk_obj){guiTests.openPage(path,env,(env)=>{return vstMakeLocalApiUrl(path,pk_obj)});guiTests.deleteObject(path);guiTests.openError404Page(env,(env)=>{return vstMakeLocalApiUrl(path,pk_obj)});}
guiTests.hasDeleteButton=function(isHas,path="hasDeleteButton")
{return guiTests.hasElement(isHas,".btn-delete-one-entity",path)}
guiTests.hasCreateButton=function(isHas,path="hasCreateButton")
{return guiTests.hasElement(isHas,".btn-create-one-entity",path)}
guiTests.hasAddButton=function(isHas,path="hasAddButton")
{return guiTests.hasElement(isHas,".btn-add-one-entity",path)}
guiTests.hasEditButton=function(isHas,path="hasEditButton")
{return guiTests.hasElement(isHas,".btn-edit-one-entity",path)}
guiTests.hasElement=function(isHas,selector,path="")
{syncQUnit.addTest("guiPaths['"+path+"'].hasElement['"+selector+"'] == "+isHas,function(assert)
{let done=assert.async();if($(selector).length!=isHas/1)
{debugger;}
assert.ok($(selector).length==isHas/1,'hasElement["'+path+'"][selector='+selector+'] has ("'+$(selector).length+'") isHas == '+isHas);testdone(done)});}
guiTests.addChildObjectToParentList=function(path,child_path,params,env,pk_obj)
{let api_obj=guiSchema.path[child_path];guiTests.openPage(child_path+"new/",env,(env)=>{return vstMakeLocalApiUrl(child_path+"new/",pk_obj)});guiTests.setValuesAndCreate(child_path+"new/",params.data,(data)=>{if(!data){return console.error("Tests depended on: '"+child_path+"new/' test will be failed because typeof data == undefined");}
env["child_"+api_obj.bulk_name+"_id"]=window.curentPageObject.getPkValueForUrl(data);env["child_"+api_obj.bulk_name+"_name"]=data.name||window.curentPageObject.getPkValueForUrl(data);pk_obj["api_child_"+api_obj.bulk_name]=env["child_"+api_obj.bulk_name+"_id"];},params.is_valid);guiTests.openPage(path,env,(env)=>{return vstMakeLocalApiUrl(path,pk_obj)});guiTests.testActionAndWaitRedirect(path,()=>{$(".btn-add-one-entity").trigger("click");});guiTests.openPage(path+"add/search/ordering=-id/",env,(env)=>{return vstMakeLocalApiUrl(path+"add/search/ordering=-id/",pk_obj)});guiTests.testActionAndWaitRedirect(path,()=>{$(".item-row.item-"+pk_obj["api_child_"+api_obj.bulk_name]+" .guiListSelections-toggle-btn").trigger("click");$(".btn_add-selected").trigger("click");});syncQUnit.addTest("guiPaths['"+path+" add child to parent's list'] ",function(assert){let done=assert.async();assert.ok($(".item-row.item-"+pk_obj["api_child_"+api_obj.bulk_name]).length>0,"child object was added to parent list");testdone(done);});guiTests.deleteObjByPath(path+"{child_"+api_obj.bulk_name+"}/",env,pk_obj);guiTests.deleteObjByPath(child_path+"{child_"+api_obj.bulk_name+"}/",env,pk_obj);}
guiTests.executeAction=function(path,params,env,pk_obj){guiTests.openPage(path,env,(env)=>{return vstMakeLocalApiUrl(path,pk_obj)});let values;let fieldsData=params.data;syncQUnit.addTest("guiPaths['"+path+"'] ",function(assert)
{let done=assert.async();if(typeof fieldsData=="function"){fieldsData=fieldsData();}
values=guiTests.setValues(assert,fieldsData);assert.ok(true);testdone(done);});guiTests.clickAndWaitRedirect(".btn_exec");guiTests.compareValues(values,fieldsData);}
guiTests.copyObjectByPath=function(path,params,env,pk_obj)
{guiTests.executeAction(path,params,env,pk_obj);if(params.save_id&&params.save_id.key){syncQUnit.addTest("guiPaths['"+path+"' save pk of copied object] ",function(assert)
{let done=assert.async();if(window.curentPageObject.model.data){env["copy_"+params.save_id.key+"_id"]=window.curentPageObject.getPkValueForUrl(window.curentPageObject.model.data);env["copy_"+params.save_id.key+"_name"]=window.curentPageObject.model.data.name||window.curentPageObject.getPkValueForUrl(window.curentPageObject.model.data);pk_obj["api_copy_"+params.save_id.key+"_id"]=env["copy_"+params.save_id.key+"_id"];assert.ok(true,"Id of copied object was saved");}else{assert.ok(false,"Id of copied object was not saved");}
testdone(done);});}
if(params.page&&params.page.delete){guiTests.deleteObject();}}
guiTests.createUser=function(env,pk_obj,is_parent){let path='/user/new/';let password=rundomString(6);let fieldsData={username:{value:rundomString(6)},email:{value:rundomString(6)+"@gmail.com"},password:{value:password,do_not_compare:true},password2:{value:password,do_not_compare:true},};guiTests.openPage(path);guiTests.setValuesAndCreate(path,fieldsData,(data)=>{let key;if(is_parent){key='api_pk';}else{key='api_user_id';}
env.user_id=data.id;env.user_name=data.username;pk_obj[key]=data.id;},true);}
guiTests.testForPath=function(path,params)
{let env={}
let api_obj=guiSchema.path[path]
guiTests.openPage(path)
guiTests.hasCreateButton(1,path)
guiTests.hasAddButton(0,path)
guiTests.openPage(path+"new")
for(let i in params.create)
{guiTests.createObject(path,params.create[i].data,env,params.create[i].is_valid)
if(params.create[i].is_valid)
{break;}
guiTests.wait();}
guiTests.openPage(path)
guiTests.openPage(path,env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path,{api_pk:env.objectId})})
guiTests.hasDeleteButton(true,path)
guiTests.hasCreateButton(false,path)
guiTests.hasAddButton(false,path)
guiTests.openPage(path,env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path,{api_pk:env.objectId})})
guiTests.openPage(path+"edit",env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path+"edit",{api_pk:env.objectId})})
for(let i in params.update)
{guiTests.updateObject(path,params.update[i].data,params.update[i].is_valid)
if(params.update[i].is_valid)
{break;}}
guiTests.deleteObject()
guiTests.openError404Page(env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path,{api_pk:env.objectId})})}
guiTests.testForPathInternalLevel=function(path,params,env,pk_obj,is_parent)
{let api_obj=guiSchema.path[path];let bool;guiTests.openPage(api_obj.path,env,(env)=>{return vstMakeLocalApiUrl(api_obj.path,pk_obj)});bool=(params.list&&params.list.hasCreateButton!==undefined)?params.list.hasCreateButton:true;guiTests.hasCreateButton(bool,api_obj.path);bool=(params.list&&params.list.hasAddButton!==undefined)?params.list.hasAddButton:false;guiTests.hasAddButton(bool,path);if(params.add_child){guiTests.addChildObjectToParentList(api_obj.path,params.add_child.path,params.add_child.create,env,pk_obj);}
for(let i in params.create){guiTests.openPage(api_obj.path+"new/",env,(env)=>{return vstMakeLocalApiUrl(api_obj.path+"new/",pk_obj)});guiTests.setValuesAndCreate(api_obj.path+"new/",params.create[i].data,(data)=>{let key;if(is_parent){key='api_pk';}else{key='api_'+api_obj.bulk_name+'_id';}
if(!data)
{return console.error("Tests depended on: '"+api_obj.path+"new/' test will be failed because typeof data == undefined");}
env[api_obj.bulk_name+"_id"]=window.curentPageObject.getPkValueForUrl(data);env[api_obj.bulk_name+"_name"]=data.name||window.curentPageObject.getPkValueForUrl(data);pk_obj[key]=env[api_obj.bulk_name+"_id"];},params.create[i].is_valid)}
guiTests.openPage(api_obj.page.path,env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path,pk_obj)});for(let i in params.update){guiTests.openPage(api_obj.page.path+"edit/",env,(env)=>{return vstMakeLocalApiUrl(api_obj.page.path+"edit/",pk_obj)});if(params.page&&params.page.wait){guiTests.wait();}
guiTests.updateObject(api_obj.page.path+"edit/",params.update[i].data,params.update[i].is_valid);}
bool=(params.page&&params.page.hasDeleteButton!==undefined)?params.page.hasDeleteButton:true;guiTests.hasDeleteButton(bool,api_obj.page.path);bool=(params.page&&params.page.hasCreateButton!==undefined)?params.page.hasCreateButton:false;guiTests.hasCreateButton(bool,api_obj.page.path);bool=(params.page&&params.page.hasAddButton!==undefined)?params.page.hasAddButton:false;guiTests.hasAddButton(bool,api_obj.page.path);if(params.page&&params.page.delete){guiTests.deleteObjByPath(api_obj.page.path,env,pk_obj);}}