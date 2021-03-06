package ctxutils

import (
	"context"
	"google.golang.org/grpc/metadata"
)

func GetMessageId(ctx context.Context) []string {
	return GetValueFromContext(ctx, messageIdKey)
}

func SetMessageId(ctx context.Context, messageId []string) context.Context {
	ctx = context.WithValue(ctx, messageIdKey, messageId)
	md, ok := metadata.FromOutgoingContext(ctx)
	if !ok {
		md = metadata.MD{}
	}
	md[messageIdKey] = messageId
	return metadata.NewOutgoingContext(ctx, md)
}

func AddMessageId(ctx context.Context, messageId ...string) context.Context {
	m := GetMessageId(ctx)
	m = append(m, messageId...)
	return SetMessageId(ctx, m)
}

func ClearMessageId(ctx context.Context) context.Context {
	return SetMessageId(ctx, []string{})
}
