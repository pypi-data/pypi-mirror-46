class View{constructor(model,schema,template){let qs_constructor=this.constructor.getQuerySetConstructor(model);this.schema=schema;this.objects=new qs_constructor(model,this.schema.path);this.template=template;this.mixins=[];}
getViewSublinkButtons(type,buttons,instance){return buttons;}
static getQuerySetConstructor(model){if(guiQuerySets[model.name+'QuerySet']){return guiQuerySets[model.name+'QuerySet'];}
return guiQuerySets['QuerySet'];}}
class ViewConstructor extends BaseEntityConstructor{constructor(openapi_dictionary,models){super(openapi_dictionary);this.models=models;}
getPaths(openapi_schema){return openapi_schema[this.dictionary.paths.name];}
getPathOperationId(path_obj_prop){return path_obj_prop[this.dictionary.paths.operation_id.name];}
getTypesOperationAlwaysToAdd(){return this.dictionary.paths.types_operations_always_to_add;}
getViewSchema_name(path){let path_parths=path.replace(/\/{[A-z]+}/g,"").split(/\//g);return path_parths[path_parths.length-2];}
getViewSchema_baseOptions(path){return{name:this.getViewSchema_name(path),level:(path.match(/\//g)||[]).length,}}
getViewSchema_filters(operation_id_filters,path_obj_prop){let filters=$.extend(true,{},path_obj_prop[operation_id_filters.name]);for(let filter in filters){if(this.dictionary.models.filters_to_delete.includes(filters[filter].name)){delete filters[filter];}}
return filters;}
generateViewSchemaFilters(operation_id_filters,path_obj_prop,path){let f_obj={};let filters=this.getViewSchema_filters(operation_id_filters,path_obj_prop);tabSignal.emit("views["+path+"].filters.beforeInit",filters);for(let filter in filters){let format=this.getFilterFormat(filters[filter]);let opt={format:format};f_obj[filters[filter].name]=new guiFields[format]($.extend(true,{},filters[filter],opt));}
tabSignal.emit("views["+path+"].filters.afterInit",filters);return f_obj;}
getFilterFormat(filter){return this.getFieldFormat(filter);}
getViewSchema_operationIdOptions(operation_id,path,path_obj_prop){let opt={operation_id:operation_id,};for(let item in this.dictionary.schema_types){if(operation_id.indexOf(item)==-1){continue;}
opt=$.extend(true,opt,this.dictionary.schema_types[item]);opt.path=path+opt.url_postfix;delete opt.url_postfix;if(opt.filters){opt.filters=this.generateViewSchemaFilters(opt.filters,path_obj_prop,opt.path,);}
return opt;}
return $.extend(true,opt,{query_type:"post",path:path,type:'action'});}
getModelNameLink(obj,max_level=0,level=0){if(!obj){return;}
if(max_level&&max_level<=level){return;}
if(typeof obj=='string'){let name=obj.match(/\/([A-z0-9]+)$/);if(name&&name[1]){return obj;}
return;}
if(typeof obj!='object'){return;}
for(let prop in obj){if(this.dictionary.models.ref_names.includes(prop)){let name=obj[prop].match(/\/([A-z0-9]+)$/);if(name&&name[1]){return obj[prop];}}
if(typeof obj[prop]=='object'){let api_obj=this.getModelNameLink(obj[prop],max_level,level+1);if(api_obj){return api_obj;}}}}
getModelName(path_obj_prop){let model_link=this.getModelNameLink(path_obj_prop);let model_name=model_link.split("/");return model_name[model_name.length-1];}
getViewSchema_model(path_obj_prop){let model_name=this.getModelName(path_obj_prop);return this.models[model_name];}
getViewTemplate(schema){let template;let base="#template_view_";["entity",schema.name].forEach(item=>{if($(base+item).length>0){template=base+item;}});return template;}
getViews(constructor,openapi_schema){let views={};let paths=this.getPaths(openapi_schema);for(let path in paths){let path_obj=paths[path];let base_options=this.getViewSchema_baseOptions(path);for(let prop in path_obj){let operation_id=this.getPathOperationId(path_obj[prop]);if(!operation_id){continue;}
let operation_id_options=this.getViewSchema_operationIdOptions(operation_id,path,path_obj[prop]);if(views[operation_id_options.path]){continue;}
let schema=$.extend(true,{},base_options,operation_id_options);let model=this.getViewSchema_model(path_obj[prop]);let template=this.getViewTemplate(schema);tabSignal.emit("views["+schema.path+"].beforeInit",{schema:schema,model:model,template:template,});views[schema.path]=new constructor(model,schema,template);tabSignal.emit("views["+schema.path+"].afterInit",{view:views[schema.path],});}}
tabSignal.emit("allViews.inited",{views:views});return views;}
internalLinkIsOperation(name,path_obj){let bool=false;['base',path_obj.schema.type].forEach(type=>{if(this.dictionary.paths.operations[type]&&this.dictionary.paths.operations[type][name]){bool=true;}});return bool;}
getInternalLinkObj_extension(name,path,path_obj,type){let obj={};let dict=this.dictionary.paths;['base',path_obj.schema.type].forEach(path_type=>{if(dict&&dict[type]&&dict[type][path_type]&&dict[type][path_type][name]){obj=$.extend(true,obj,dict[type][path_type][name]);}});return obj;}
isPathObjSchemaEmpty(path_obj){if(path_obj.schema.empty){return true;}
return isEmptyObject(path_obj.objects.model.fields);}
getInternalLinkObj(name,path,path_obj,type){let obj={name:name,};if(!(path_obj.schema.hidden)&&path){obj.path=path;}
if(this.isPathObjSchemaEmpty(path_obj)){obj.empty=true;obj.query_type=path_obj.schema.query_type;}
obj=$.extend(true,obj,this.getInternalLinkObj_extension(name,path,path_obj,type),);return obj;}
getViewInternalLinks(views,path){let links={actions:{},operations:{},sublinks:{},child_links:{},};for(let link in views){if(link==path){continue;}
if(link.indexOf(path)!=0){continue;}
let link_name=link.match(/\/([A-z0-9]+)\/$/);if(!link_name){continue;}
link_name=link_name[1];let dif=link.match(/\//g).length-path.match(/\//g).length;let link_type;if(dif>2){continue;}
if(dif==2){link_type='child_links';}else{if(views[link].schema.type=='action'){link_type='actions';}else if(this.internalLinkIsOperation(link_name,views[path])){link_type='operations';}else{link_type='sublinks';}}
if(link_type){links[link_type][link_name]=this.getInternalLinkObj(link_name,link,views[link],link_type);}}
let types_to_add=this.getTypesOperationAlwaysToAdd();if(types_to_add.includes(views[path].schema.type)){let dict=this.dictionary.paths;let path_type=views[path].schema.type;Object.keys(links).forEach(link_type=>{if(dict&&dict[link_type]&&dict[link_type][path_type]){for(let link in dict[link_type][path_type]){if(links[link_type][link]){continue;}
links[link_type][link]=dict[link_type][path_type][link];}}});}
if(views[path].schema.type=="list"&&views[path].schema.level>2&&views["/"+views[path].schema.name+"/"]){let dict=this.dictionary.paths;let list_op;if(dict&&dict.operations&&dict.operations.list){list_op=dict.operations.list;let opt={list_paths:["/"+views[path].schema.name+"/"],};links.operations.add=$.extend(true,{},list_op.add,opt);}}
return links;}
getViewMultiActions(views,path){let multi_actions={};let dict=this.dictionary.paths;let list=views[path];if(!list.schema.page_path){return;}
let page=views[list.schema.page_path];['actions','operations'].forEach(op_type=>{if(!page.schema[op_type]){return;}
for(let item in page.schema[op_type]){if(dict&&dict.multi_actions&&dict.multi_actions.includes(item)){multi_actions[item]=$.extend(true,{multi_action:true,},page.schema[op_type][item]);}}});return multi_actions;}
connectPageAndListViews(views,page_path){let list_path=page_path.replace(/\{[A-z]+\}\/$/,"");if(views[list_path]){views[page_path].schema.list_path=list_path;views[list_path].schema.page_path=page_path;}}
generateViews(constructor,openapi_schema){let views=this.getViews(constructor,openapi_schema);for(let path in views){let links=this.getViewInternalLinks(views,path);for(let key in links){views[path].schema[key]=links[key];}
if(views[path].schema.type=='page'){this.connectPageAndListViews(views,path);}}
for(let path in views){if(views[path].schema.type=='list'){views[path].schema.multi_actions=this.getViewMultiActions(views,path);}
if(views[path].schema.hidden){delete views[path];}
tabSignal.emit("views["+path+"].created",{view:views[path]});}
tabSignal.emit("allViews.created",{views:views});return views;}}