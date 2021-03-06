package redis

import (
	"PROJECT_46ea591951824d8e9376b0f98fe4d48a/pkg/logger"
	"github.com/go-redis/redis"
)

type RedisClient struct {
	client *redis.Client
}

func NewRedisClientOrDie(options *RedisOptions, stopCh <-chan struct{}) *RedisClient {
	client, err := NewRedisClient(options, stopCh)
	if err != nil {
		panic(err)
	}

	return client
}

func NewRedisClient(option *RedisOptions, stopCh <-chan struct{}) (*RedisClient, error) {
	var r RedisClient

	options, err := redis.ParseURL(option.RedisURL)

	if err != nil {
		logger.Error(nil, err.Error())
		return nil, err
	}

	r.client = redis.NewClient(options)

	if err := r.client.Ping().Err(); err != nil {
		logger.Error(nil, "unable to reach redis host", err)
		r.client.Close()
		return nil, err
	}

	if stopCh != nil {
		go func() {
			<-stopCh
			if err := r.client.Close(); err != nil {
				logger.Error(nil, err.Error())
			}
		}()
	}

	return &r, nil
}

func (r *RedisClient) Redis() *redis.Client {
	return r.client
}
