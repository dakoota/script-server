<template>
    <div class="welcome-panel">
        <img :src="imageSrc" alt="script server logo">
        <div class="welcome-text">
            Welcome to the jungle. <br> Expect a headache or two.
        </div>
        <div class="welcome-cookie-text" ref="welcomeCookieText">
            ¯\_(ツ)_/¯
        </div>
    </div>
</template>

<script>
    const defaultImageSrc = 'images/console.png';
    const cookieImageSrc = 'images/cookie.png';

    export default {
        name: 'AppWelcomePanel',
        data() {
            return {
                'imageSrc': defaultImageSrc
            }
        },

        mounted: function () {
            const welcomeCookiePanel = this.$refs.welcomeCookieText;
            welcomeCookiePanel.addEventListener('mouseover', () => {
                this.imageSrc = cookieImageSrc;
            });

            welcomeCookiePanel.addEventListener('mouseout', () => {
                this.imageSrc = defaultImageSrc;
            });
        }

    }
</script>

<style scoped>
    .welcome-panel {
        flex: 1;
        color: #9e9e9e;
        display: flex;
        text-align: center;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        height: 100%;
        overflow: hidden;
    }

    .welcome-text {
        margin-top: 15px;
    }

    .welcome-cookie-text {
        margin-top: 8px;
    }
</style>
