<template>
  <div>
    <h1>{{ loading }}</h1>
    <h1>{{ data }}</h1>
  </div>
</template>

<script>
import { getHello } from '@/api/hello'
import { PageView } from '@/layouts'

export default {
  name: 'HelloWorld',
  components: {
    PageView,
  },
  data() {
    return {
      data: [],
      loading: false,
    }
  },
  mounted() {
    this.fetch()
  },
  watch: {
    $route(to, from) {
      this.fetch()
    },
  },
  computed: {
    title() {
      return `hello, world`
    },
  },
  methods: {
    fetch() {
      this.loading = true
      return getHello()
        .then((data) => {
          this.loading = false
          this.data = data
        })
        .catch((err) => {
          this.$notification.error({
            duration: null,
            message: err,
          })
          this.loading = false
        })
    },
  },
}
</script>
