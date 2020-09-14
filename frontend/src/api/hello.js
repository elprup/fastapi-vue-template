import { axios } from '@/utils/request'

const api = {
  Hello: 'hello'
}

export default api

export function getHello() {
  return axios.get(api.Hello, {})
}
