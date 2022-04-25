<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  },
};
</script>

<style>
  .main-card-body {
    height: 60vh;
    overflow-y: scroll;
  }

  .main-card {
    width: 95vw;
    min-height: 85vh;
  }

  .main-modal {
    width:80vw;
    height: 80vh;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
  }

  .main-modal-body {
    flex-grow: fill;
  }
</style>
