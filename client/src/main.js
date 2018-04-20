// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios';
import global_ from '@/commons/Global';
import VueHighlightJS from 'vue-highlight.js';

import 'element-ui/lib/theme-chalk/index.css'
import 'highlight.js/styles/github.css';


import {
  Pagination,
  Dialog,
  Autocomplete,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Menu,
  Submenu,
  MenuItem,
  MenuItemGroup,
  Input,
  InputNumber,
  Radio,
  RadioGroup,
  RadioButton,
  Checkbox,
  CheckboxButton,
  CheckboxGroup,
  Switch,
  Select,
  Option,
  OptionGroup,
  Button,
  ButtonGroup,
  Table,
  TableColumn,

  Popover,
  Tooltip,

  Form,
  FormItem,
  Tabs,
  TabPane,
  Tag,

  Slider,
  Icon,
  Row,
  Col,

  Card,

  Carousel,
  CarouselItem,
  Collapse,
  CollapseItem,
  Container,
  Header,
  Main,
  Footer,
  Loading,
  MessageBox,
  Message,
  Notification
} from 'element-ui';

Vue.use(Pagination);
Vue.use(Dialog);
Vue.use(Autocomplete);
Vue.use(Dropdown);
Vue.use(DropdownMenu);
Vue.use(DropdownItem);
Vue.use(Menu);
Vue.use(Submenu);
Vue.use(MenuItem);
Vue.use(MenuItemGroup);
Vue.use(Input);
Vue.use(InputNumber);
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.use(RadioButton);
Vue.use(Checkbox);
Vue.use(CheckboxButton);
Vue.use(CheckboxGroup);
Vue.use(Switch);
Vue.use(Select);
Vue.use(Option);
Vue.use(OptionGroup);
Vue.use(Button);
Vue.use(ButtonGroup);
Vue.use(Table);
Vue.use(TableColumn);

Vue.use(Popover);
Vue.use(Tooltip);

Vue.use(Form);
Vue.use(FormItem);
Vue.use(Tabs);
Vue.use(TabPane);
Vue.use(Tag);

Vue.use(Slider);
Vue.use(Icon);
Vue.use(Row);
Vue.use(Col);


Vue.use(Card);

Vue.use(Carousel);
Vue.use(CarouselItem);
Vue.use(Collapse);
Vue.use(CollapseItem);

Vue.use(Container);
Vue.use(Header);
Vue.use(Main);
Vue.use(Footer);


Vue.prototype.$loading = Loading.service;
Vue.prototype.$message = Message;

Vue.use(VueHighlightJS);
Vue.config.productionTip = false;
Vue.prototype.$ELEMENT = { size: 'small' };
Vue.prototype.axios = axios;
Vue.prototype.GLOBAL = global_;

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
});
