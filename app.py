import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:  # Check if a file has been uploaded
    bytes_data = uploaded_file.getvalue()

# To read file as bytes:

    # CONVERTING STREAM FILE INTO STRING
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')  # to remove group_notification from dropdown
    user_list.sort()  # to sort user list in ascending order
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # TOP STATISTICS ------------------------------

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

    #   MONTHLY TIMELINE ------------
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = "green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    #   DAILY TIMELINE ------------------
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    #   ACTIVITY MAP --------------------
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values, color='brown')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    # ACTIVITY HEATMAP
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


    # FINDING BUSIEST USERS IN THE "GROUP"

        if selected_user == "Overall":
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            st.title('Most Busy Users')

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


    # WORD CLOUD
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    # MOST COMMON WORDS
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='green')
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(most_common_df)

    # EMOJI ANALYSIS
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)


# Sentiment Analysis
        sentiment = helper.sentiment_analysis(selected_user, df)
        ax.barh(sentiment[0], sentiment[1], color='green')
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        st.write(f"Sentiment for {selected_user}: {sentiment}")











