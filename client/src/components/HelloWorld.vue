<template>
    <h1>HELLO WORLD!!!</h1>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      drawer: null,
      items: [
        { title: 'Home', icon: 'mdi-view-dashboard' },
        { title: 'About', icon: 'mdi-forum' },
      ],
    };
  },
};
</script>
