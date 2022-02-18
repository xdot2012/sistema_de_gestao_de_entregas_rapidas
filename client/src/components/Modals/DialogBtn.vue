<template>
  <v-dialog max-width="95%">
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="primary"
          v-bind="attrs" v-on="on">{{ name }}</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class=" pa-8">
          <v-card-title>
            <v-btn text @click="dialog.value = false">Close</v-btn>
          </v-card-title>
          {{ template }}
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
export default {
  name: 'DialogButton',
  data() {
    return {
      name: null,
      template: null,
    };
  },
};
</script>

<style>
</style>
