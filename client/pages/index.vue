<script setup>
definePageMeta({
  middleware: "authenticated-only",
});
</script>

<template>
  <v-container>
    <v-row justify="cneter">
      <v-col md="8" offset-md="2">
        <h1>About</h1>
        <p>
          This is a simple banking app. You can create accounts, transfer money
          between them, and see the transaction history. Also, this app supports
          real-time notifications about transactions.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8" offset="2">
        <v-divider />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="3" offset="1">
        <h2>Backend</h2>
        <v-list>
          <v-list-item>FastApi</v-list-item>
          <v-list-item>PostgreSQL</v-list-item>
          <v-list-item>SqlAlchemy</v-list-item>
          <v-list-item>Kafka</v-list-item>
          <v-list-item>Nginx</v-list-item>
        </v-list>
      </v-col>

      <v-col cols="3">
        <h2>Frontend</h2>
        <ul>
          <v-list-item>Vue</v-list-item>
          <v-list-item>Nuxt</v-list-item>
          <v-list-item>Vuetify</v-list-item>
          <v-list-item>pinia</v-list-item>
        </ul>
      </v-col>

      <v-col cols="3">
        <h2>DevOps</h2>
        <v-list>
          <v-list-item>Docker</v-list-item>
          <v-list-item>Nginx</v-list-item>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8" offset="2">
        <v-divider />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8" offset="2">
        <h2>Features</h2>
        <v-list density="compact">
          <v-list-item>Signing up/in/out</v-list-item>
          <v-list-item>Real-time notifications</v-list-item>
          <v-list-item>Account creation</v-list-item>
          <v-list-item>Money transfer</v-list-item>
          <v-list-item>Transaction history</v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>
