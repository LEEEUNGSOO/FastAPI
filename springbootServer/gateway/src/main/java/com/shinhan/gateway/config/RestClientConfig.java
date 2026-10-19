package com.shinhan.gateway.config;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration                                                   // 설정 클래스
public class RestClientConfig {

    @Bean                                                        // 리턴값을 Spring이 보관 → 필요한 곳에 주입
    public RestClient fastApiClient(RestClient.Builder builder,  // Spring Boot가 만들어 둔 빌더
                                    @Value("${fastapi.base-url}") String baseUrl) {   // yml 값 읽기
        return builder
                .baseUrl(baseUrl)                                // 앞 주소 http://localhost:8000 고정
                .build();
    }
}

/* ===== 전체 이해 =====
 * - FastAPI 전용 RestClient를 하나 만들어 Bean으로 등록합니다.
 * - baseUrl을 미리 넣어 두었으니 컨트롤러에서는 "/accounts/..." 뒷부분만 씁니다.
 * - 주소는 application.yml의 fastapi.base-url 에서 가져옵니다. (코드에 박지 않기)
 * - RestClient.Builder 를 주입받아 쓰면 Spring Boot의 Jackson 설정(LocalDate 변환,
 *   모르는 JSON 키 무시)이 그대로 따라옵니다.
 * - 누가 쓰나: AccountController 생성자로 들어감 (파라미터 이름 fastApiClient)
 */