function getProfileString(){return'profile';}
var profile_mixins={};profile_mixins['/user/{'+path_pk_key+'}/']={methods:{getBreadcrumbNameForCurrentPath:getProfileString,},computed:{title:getProfileString,},};profile_mixins['/user/{'+path_pk_key+'}/edit/']={computed:{title:getProfileString,},};class ProfileViewConsctuctor{constructor(profile_mixins){this.mixins=profile_mixins;}
generateProfileView(views,path){let view=views[path];let new_view=new View(view.objects.model,$.extend(true,{},view.schema),view.template,);let mixin=this.getBaseProfileMixin(path);if(this.mixins[path]){mixin=$.extend(true,mixin,this.mixins[path]);}
if(view.schema.type=='page_edit'){mixin.methods.getRedirectUrl=function(opt){return this.$route.path.replace('/edit',"");}}
new_view.mixins=[...view.mixins];new_view.mixins.push(mixin);return new_view;}
getBaseProfileMixin(path){return{computed:{url(){return path.replace('{'+path_pk_key+'}',my_user_id);}},methods:{loadParentInstanceOrNot(views,obj){if(views[obj.path]&&views[obj.path].schema.type=="list"){return false;}
if(obj.path=='/profile/'){return false;}
return true;},getParentInstancesForPath(){let inner_paths=this.getParentPaths(this.$route.name,this.$route.path);let views=this.$store.getters.getViews;for(let index in inner_paths){let obj=inner_paths[index];if(!this.loadParentInstanceOrNot(views,obj)){continue;}
let url=obj.url.replace('profile','user/'+my_user_id);this.getInstance(views[obj.path],url).then(instance=>{this.data.parent_instances[obj.url]=instance;this.data.parent_instances={...this.data.parent_instances};}).catch(error=>{debugger;});}},},};}}
var profile_constructor=new ProfileViewConsctuctor(profile_mixins);function addProfileViews(obj){let str='/user/{'+path_pk_key+'}/';let views=obj.views;let paths_for_profile=Object.keys(views).filter(path=>path.indexOf(str)==0);paths_for_profile.forEach(path=>{let new_path=path.replace('user/{'+path_pk_key+'}','profile');let new_view=profile_constructor.generateProfileView(views,path);views[new_path]=new_view;});}
class Gravatar{constructor(opt={}){this.base_url='https://www.gravatar.com/avatar/{hash}?d=mp';if(opt.base_url){this.base_url=opt.base_url;}
this.default_gravatar=window.guiStaticPath+'img/anonymous.png';}
getDefaultGravatar(){return this.default_gravatar;}
getGravatarByEmail(email){if(!email){return this.getDefaultGravatar();}
return this.base_url.format({hash:md5(email)});}}
function userModelHandler(obj){obj.model.view_name='username';}
var userModels=['OneUser','User'];userModels.forEach(model=>{let signal="models[{0}].created".format([model]);tabSignal.connect(signal,userModelHandler);});tabSignal.connect('models[User].fields.beforeInit',fields=>{fields.email.hidden=true;});['CreateUser','ChangePassword'].forEach(model=>{tabSignal.connect('models[{0}].fields.beforeInit'.format([model]),fields=>{['old_password','password','password2'].forEach(field=>{if(fields[field]){fields[field].format='password';}});});});tabSignal.connect('allViews.inited',addProfileViews);