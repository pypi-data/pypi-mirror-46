

from ..utils import Object


class Update(Object):
    """
    Contains notifications about data changes

    No parameters required.
    """
    ID = "update"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UpdateBasicGroupFullInfo or UpdateUnreadChatCount or UpdateNewCustomQuery or UpdateUserPrivacySettingRules or UpdateChatReplyMarkup or UpdateMessageViews or UpdateChatIsPinned or UpdateScopeNotificationSettings or UpdateFile or UpdateUserFullInfo or UpdateUnreadMessageCount or UpdateMessageEdited or UpdateLanguagePackStrings or UpdateChatIsMarkedAsUnread or UpdateNewChat or UpdateChatIsSponsored or UpdateNotificationGroup or UpdateNewInlineQuery or UpdateMessageContent or UpdateDeleteMessages or UpdateNewCallbackQuery or UpdateChatPinnedMessage or UpdateFileGenerationStop or UpdateNewChosenInlineResult or UpdateChatTitle or UpdateMessageSendFailed or UpdateChatUnreadMentionCount or UpdateBasicGroup or UpdateMessageSendAcknowledged or UpdateMessageMentionRead or UpdateChatReadOutbox or UpdateNewCustomEvent or UpdateMessageContentOpened or UpdateChatPhoto or UpdateActiveNotifications or UpdateChatNotificationSettings or UpdateUserStatus or UpdateChatOrder or UpdateSecretChat or UpdateFileGenerationStart or UpdateCall or UpdateUserChatAction or UpdateTermsOfService or UpdateNewShippingQuery or UpdateChatDraftMessage or UpdateOption or UpdateNewInlineCallbackQuery or UpdateNotification or UpdateAuthorizationState or UpdateHavePendingNotifications or UpdateChatReadInbox or UpdateChatDefaultDisableNotification or UpdateChatOnlineMemberCount or UpdateSupergroupFullInfo or UpdateFavoriteStickers or UpdateMessageSendSucceeded or UpdateNewPreCheckoutQuery or UpdateConnectionState or UpdateChatLastMessage or UpdateNewMessage or UpdateServiceNotification or UpdateInstalledStickerSets or UpdateTrendingStickerSets or UpdateRecentStickers or UpdatePoll or UpdateSupergroup or UpdateUser or UpdateSavedAnimations":
        if q.get("@type"):
            return Object.read(q)
        return Update()
