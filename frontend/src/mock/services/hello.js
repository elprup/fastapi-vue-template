import Mock from 'mockjs2'
import { builder } from '../util'

//
const hello = () => {
  return builder([{ value: 200, name: 'my hello world' }])
}

Mock.mock(/\/hello/, 'get', hello)
