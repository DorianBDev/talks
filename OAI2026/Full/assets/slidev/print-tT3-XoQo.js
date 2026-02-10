import{d as _,a4 as u,z as h,f as n,g as t,t as s,T as c,F as f,aj as g,o as l,i as v,e as x,ad as b}from"../modules/vue-Dg5UiXBU.js";import{a as y,u as N,x as m}from"../index-Wihcs2a9.js";import{_ as k}from"./NoteDisplay.vue_vue_type_style_index_0_lang-DKyqt5Md.js";import"../modules/shiki-C_3u9Tgf.js";const T={id:"page-root"},w={class:"m-4"},L={class:"mb-10"},V={class:"text-4xl font-bold mt-2"},B={class:"opacity-50"},H={class:"text-lg"},S={class:"font-bold flex gap-2"},j={class:"opacity-50"},z={key:0,class:"border-main mb-8"},A=_({__name:"print",setup(C){const{slides:d,total:p}=y();u(`
@page {
  size: A4;
  margin-top: 1.5cm;
  margin-bottom: 1cm;
}
* {
  -webkit-print-color-adjust: exact;
}
html,
html body,
html #app,
html #page-root {
  height: auto;
  overflow: auto !important;
}
`),N({title:`Notes - ${m.title}`});const i=h(()=>d.value.map(o=>{var a;return(a=o.meta)==null?void 0:a.slide}).filter(o=>o!==void 0&&o.noteHTML!==""));return(o,a)=>(l(),n("div",T,[t("div",w,[t("div",L,[t("h1",V,s(c(m).title),1),t("div",B,s(new Date().toLocaleString()),1)]),(l(!0),n(f,null,g(i.value,(e,r)=>(l(),n("div",{key:r,class:"flex flex-col gap-4 break-inside-avoid-page"},[t("div",null,[t("h2",H,[t("div",S,[t("div",j,s(e==null?void 0:e.no)+"/"+s(c(p)),1),b(" "+s(e==null?void 0:e.title)+" ",1),a[0]||(a[0]=t("div",{class:"flex-auto"},null,-1))])]),x(k,{"note-html":e.noteHTML,class:"max-w-full"},null,8,["note-html"])]),r<i.value.length-1?(l(),n("hr",z)):v("v-if",!0)]))),128))])]))}});export{A as default};
