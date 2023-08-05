(window.webpackJsonp=window.webpackJsonp||[]).push([[63],{167:function(t,e,a){"use strict";var s=a(8);e.a=Object(s.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},673:function(t,e,a){"use strict";a.r(e);var s=a(4),c=a(22),i=a(167),o=a(67);customElements.define("notification-manager",class extends(Object(i.a)(c.a)){static get template(){return s.a`
      <style>
        paper-toast {
          z-index: 1;
        }
      </style>

      <ha-toast
        id="toast"
        dir="[[_rtl]]"
        no-cancel-on-outside-click="[[_cancelOnOutsideClick]]"
      ></ha-toast>
    `}static get properties(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1},_rtl:{type:String,computed:"_computeRTLDirection(hass)"}}}ready(){super.ready(),Promise.all([a.e(1),a.e(29)]).then(a.bind(null,400))}showDialog({message:t}){this.$.toast.show(t)}_computeRTLDirection(t){return Object(o.a)(t)?"rtl":"ltr"}})}}]);