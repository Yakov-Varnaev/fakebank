<template>
  <v-app>
    <app-bar />
    <v-main>
      <v-container fluid class="fill-height">
        <v-row justify="center">
          <slot />
        </v-row>
      </v-container>
    </v-main>
    <alert-container />
  </v-app>
</template>
