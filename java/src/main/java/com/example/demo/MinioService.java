package com.example.demo;


import io.minio.*;
import io.minio.errors.*;
import io.minio.messages.Bucket;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.util.List;

@Service
public class MinioService {

    private final MinioClient minioClient;

    @Value("${minio.bucket-name}")
    private String bucketName;

    public MinioService(MinioClient minioClient) {
        this.minioClient = minioClient;
    }

    public void uploadFile(String fileName, MultipartFile file) throws Exception {
        // Ensure the bucket exists
        // var bucketNameArgs = BucketExistsArgs.builder().bucket(bucketName).build();
        // if (!minioClient.bucketExists(bucketNameArgs)) {
        // minioClient.makeBucket(bucketNameArgs);
        // }

        // Upload the file
        minioClient.putObject(
                    PutObjectArgs.builder()
                        .bucket(bucketName)
                        .object(fileName)
                        .stream(file.getInputStream(), file.getSize(), -1)
                        .contentType(file.getContentType())
                        .build()
                );
    }

    public InputStream getFile(String fileName) throws Exception {
        return minioClient.getObject(GetObjectArgs.builder()
                .bucket(bucketName)
                .object(fileName)
                .build());
    }

    public void deleteFile(String fileName) throws Exception {
        minioClient.removeObject(
                RemoveObjectArgs.builder()
                .bucket(bucketName)
                .object(fileName)
                .build()
                );
    }
}
